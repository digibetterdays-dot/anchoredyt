#!/usr/bin/env python3
"""Word timings from a KNOWN script + its voiceover, without speech recognition.

Fallback for when `hyperframes transcribe` can't run (e.g. the model host is
blocked). It works because a read script pauses at punctuation:
  1. ffmpeg silencedetect finds the pauses in the audio;
  2. dynamic programming matches pauses to punctuation breaks in the text,
     choosing the matching whose speech stretches best fit a constant speaking
     rate (pauses may be skipped, e.g. stops inside words; breaks may be
     unvoiced, e.g. a light comma);
  3. words inside each stretch are spaced by character count.

Accuracy: sentence and clause starts land on real pauses; words mid-clause are
interpolated (typically within ~0.3 s on clean TTS/studio audio). The
VO must follow the script; ad-libs or re-takes break the alignment.

usage: python3 -I align_text.py <script.txt> <voice.wav> -o words.json [--noise -40] [--min-pause 0.12]
"""
import argparse, json, re, subprocess, sys

BREAK = {".": 1.0, "?": 1.0, "!": 1.0, ":": 0.7, ";": 0.7, ",": 0.45, "—": 0.5, ")": 0.3}


def pauses(wav, noise, dmin):
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", wav, "-af",
                          f"silencedetect=noise={noise}dB:d={dmin}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    dur = float(re.search(r"Duration: (\d+):(\d+):([0-9.]+)", err).expand(r"\1")) * 3600 + \
        float(re.search(r"Duration: (\d+):(\d+):([0-9.]+)", err).group(2)) * 60 + \
        float(re.search(r"Duration: (\d+):(\d+):([0-9.]+)", err).group(3))
    if len(en) < len(st):
        en.append(dur)
    return list(zip(st, en)), dur


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script"); ap.add_argument("wav"); ap.add_argument("-o", required=True)
    ap.add_argument("--noise", default="-40"); ap.add_argument("--min-pause", type=float, default=0.12)
    a = ap.parse_args()

    text = open(a.script, encoding="utf-8").read()
    paras = [p.split() for p in re.split(r"\n\s*\n", text) if p.strip()]
    words, para_end = [], set()
    for p in paras:
        words += p
        para_end.add(len(words) - 1)
    clen = [len(re.sub(r"\W", "", w)) + 1 for w in words]
    cum = [0]
    for c in clen:
        cum.append(cum[-1] + c)

    # candidate breaks: after word k (boundary index k+1 in cum terms)
    cand = [0]
    weight = {0: 1.0}
    for k, w in enumerate(words):
        wt = 1.2 if k in para_end else max([BREAK.get(ch, 0) for ch in w[-2:]] + [0])
        if wt and k + 1 < len(words):
            cand.append(k + 1); weight[k + 1] = wt
    cand.append(len(words)); weight[len(words)] = 1.0

    P, total = pauses(a.wav, a.noise, a.min_pause)
    # leading / trailing silence become the start / end anchors
    lead = P[0][1] if P and P[0][0] < 0.05 else 0.0
    inner = [p for p in P if p[0] > lead + 0.01 and p[1] < total - 0.05]
    tail = P[-1][0] if P and P[-1][1] >= total - 0.05 else total
    marks = [(lead, lead)] + inner + [(tail, tail)]          # pause j: (start, end)
    speech = (tail - lead) - sum(e - s for s, e in inner)
    rate = speech / cum[-1]                                   # seconds per char

    m, n = len(marks), len(cand)
    INF = float("inf")
    for _ in range(2):                                         # refit the rate once
        best = [[INF] * n for _ in range(m)]
        back = [[None] * n for _ in range(m)]
        best[0][0] = 0.0
        for j in range(1, m):
            for jp in range(max(0, j - 5), j):
                skipped = marks[jp + 1:j]
                skip_cost = sum(2.0 * (e - s) + 0.1 for s, e in skipped)
                audio = marks[j][0] - marks[jp][1] - sum(e - s for s, e in skipped)
                for ci in range(1, n):
                    for cp in range(max(0, ci - 8), ci):
                        b = best[jp][cp]
                        if b == INF:
                            continue
                        exp = (cum[cand[ci]] - cum[cand[cp]]) * rate
                        miss = sum(weight[cand[x]] * 0.6 for x in range(cp + 1, ci))
                        c = b + (audio - exp) ** 2 / (exp + 0.3) + miss + skip_cost + (1 - weight[cand[ci]]) * 0.8
                        if c < best[j][ci]:
                            best[j][ci] = c; back[j][ci] = (jp, cp)
        if best[m - 1][n - 1] == INF:
            sys.exit("alignment failed: check that the audio follows the script")
        path, st = [], (m - 1, n - 1)
        while st:
            path.append(st); st = back[st[0]][st[1]]
        path.reverse()
        # refit rate from matched stretches
        tot_a = tot_c = 0
        for (j0, c0), (j1, c1) in zip(path, path[1:]):
            sk = marks[j0 + 1:j1]
            tot_a += marks[j1][0] - marks[j0][1] - sum(e - s for s, e in sk)
            tot_c += cum[cand[c1]] - cum[cand[c0]]
        rate = tot_a / tot_c

    out, resid = [], []
    for (j0, c0), (j1, c1) in zip(path, path[1:]):
        t0, t1 = marks[j0][1], marks[j1][0]
        k0, k1 = cand[c0], cand[c1]
        sk = marks[j0 + 1:j1]
        audio = t1 - t0 - sum(e - s for s, e in sk)
        exp = (cum[k1] - cum[k0]) * rate
        resid.append(abs(audio - exp) / max(exp, 0.3))
        chars = cum[k1] - cum[k0]
        t = t0
        for k in range(k0, k1):
            d = (t1 - t0) * clen[k] / chars
            out.append({"id": f"w{k}", "text": words[k], "start": round(t, 3), "end": round(t + d * 0.92, 3)})
            t += d
    json.dump(out, open(a.o, "w", encoding="utf-8"), indent=0)
    resid.sort()
    print(f"{len(out)} words, {len(path) - 1} stretches matched to {len(inner)} detected pauses; "
          f"rate {1 / rate:.1f} chars/s")
    print(f"fit error per stretch: median {resid[len(resid) // 2]:.0%}, 90th pct {resid[int(len(resid) * .9)]:.0%}, "
          f"worst {resid[-1]:.0%}")
    bad = [i for i, r in enumerate(resid) if r > 0.5]
    if bad:
        print(f"WARNING: {len(bad)} stretches fit poorly (>50%): the VO may differ from the script there")


if __name__ == "__main__":
    main()
