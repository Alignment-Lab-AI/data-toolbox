# Project Roadmap

## An intro for dummies

If you're not familiar with all the theory/technology behind the project, here's a super simplified rundown:

- There are "text generation AIs" that are freely available for researchers. These are called open-source LMs (language models).
- Modern chatbots are usually made by taking a language model and "fine-tuning" it, which basically just means feeding it data similar to what you want it to generate.
  - In our case, this means fine-tuning it with conversation and roleplay data (research usually calls this "dialogue data", and they call models fine-tuned on dialogue data "dialogue models").
- LMs can have different "sizes". For example, Meta's OPT language model is offered in 125m, 350m, 1.3B, 2.7B, 6.7B, 30B and 66B sizes (where "m" = million and "B" = billion parameters).
  - The bigger the model, the better its quality. However, the more hardware you need to fine-tune and use it. And when I say more, I don't mean a couple more gigabytes of system RAM, I mean going from a single 6GB GPU to hundreds of 80GB GPUs.


So, knowing the above, our main "top-level"/medium-term objective at the moment is to get as much good quality data as we can, and fine-tune the biggest model we can. From there, we can play around with the models and see what the results are like, then debate and decide how to move forward.

---

For anyone who's interested in the actual details, here's a TL;DR version of the project's current roadmap at the task level:

## Current Status

- We have all the tooling to build a dataset from various sources, fine-tune a pre-trained LM on that dataset, and then run inference on checkpoints saved during the fine-tune process.
  - All of that tooling can be found within this repository.
- We have taken a small model, Meta's OPT-350m, and fine-tuned it on a small dataset we've built with the tooling described above. We've released it as a tiny prototype.
  - The model checkpoint is hosted on HuggingFace under [Pygmalion-AI/pygmalion-350m](https://huggingface.co/Pygmalion-AI/pygmalion-350m).
  - **Note:** Inference should not be done on the regular HuggingFace web UI since we need to do some prompt trickery and response parsing. To play around with the model, [try out this notebook](https://colab.research.google.com/drive/1K55_MCagEDD9EmWhjCi3Bm66vJM88m6P?usp=sharing).
- We have written a [userscript which can anonymize and dump your CharacterAI chats](./extras/characterai-dumper/), and made [a website where you can upload them](https://dump.nopanda.io/) to be used as training data for future models. If you're interested in contributing, please read through [this Rentry](https://rentry.org/f8peb) for more information.

## Next Steps

- We will attempt to fine-tune OPT-1.3B. For that, we'll need:
  - More hardware, which we'll probably rent out in the cloud;
  - More high-quality data, which will hopefully be covered by the contributed CAI logs and some other good datasets we can get our hands on.