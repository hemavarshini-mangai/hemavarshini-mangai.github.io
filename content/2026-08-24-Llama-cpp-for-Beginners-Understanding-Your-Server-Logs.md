Title: Llama.cpp for Beginners: Understanding Your Server Logs
Date: 2026-08-24
Category: 
Tags: 
Slug: Llama.cpp-for-Beginners:-Understanding-Your-Server-Logs
------------
A SAMPLE LOG
------------

Here's what a typical startup and inference run looks like on Windows:

0.02.229.730 I cmn  common_param: common_params_print_info: verbosity = 3
0.02.230.814 W srv  llama_server: -----------------
0.02.230.822 W srv  llama_server: CORS is set to allow all origins ('*') and no API key is set
Downloading gemma-3-1b-it-Q4_K_M.gguf ────────────────────────────── 100%
1.45.268.200 I srv    load_model: loading model 'ggml-org/gemma-3-1b-it-GGUF'
1.57.452.210 I srv    load_model: initializing, n_slots = 4, n_ctx_slot = 32768
1.57.452.227 I srv  llama_server: listening on http://127.0.0.1:8080
11.15.975.892 I slot launch_slot_: id  3 | task 0 | processing task, is_child = 0
11.27.336.963 I slot print_timing: id  3 | task 0 | prompt processing, n_tokens = 10
11.41.582.421 I slot print_timing: id  3 | task 0 | n_gen = 100, tg = 16.16 t/s, tg_3s = 16.33 t/s
12.07.342.273 I slot print_timing: id  3 | task 0 | prompt eval time = 19480.83 ms / 14 tokens
12.07.342.322 I slot print_timing: id  3 | task 0 |        eval time = 31885.09 ms / 512 tokens
12.07.342.326 I slot print_timing: id  3 | task 0 |       total time = 51365.92 ms / 526 tokens
12.07.342.330 I slot print_timing: id  3 | task 0 |    graphs reused = 509

Let's decode this piece by piece.

------------------------------------------------------------
READING THE PREFIX
------------------------------------------------------------

Every line starts with a timestamp, a log level (I for info, W for
warning), and a module tag. The tags tell you which part of
llama.cpp generated the message:

  cmn  - the common/shared utility code, mostly used for printing
         configuration info at startup.
  srv  - the server component itself: handles startup, model
         loading, and network listening.
  slot - an individual inference "slot." Llama.cpp's server can
         process multiple requests at once, and each one is assigned
         to a slot. Your log shows n_slots = 4, meaning the server
         can juggle up to four concurrent requests.

------------------------------------------------------------
UNDERSTANDING TASKS AND SLOTS
------------------------------------------------------------

When you send a prompt to the server, it becomes a task. Each task
gets a numeric ID starting at 0, and is handed off to a free slot:

  id  3 | task 0 | processing task

This line means: slot #3 has picked up task #0 and started working
on it. If you send several requests at once, you'd see different
task numbers assigned to different slots, all logging in parallel.

------------------------------------------------------------
THE TWO PHASES OF INFERENCE
------------------------------------------------------------

Every request goes through two distinct phases, and the logs report
timing for both separately.

1. PROMPT PROCESSING (a.k.a. "prompt eval")

This is where the model reads and encodes your input prompt. It
happens once per request, and its speed is reported in tokens per
second:

  prompt eval time = 19480.83 ms / 14 tokens
  (1391.49 ms per token, 0.72 tokens per second)

2. TEXT GENERATION (a.k.a. "eval" or "tg")

This is the actual generation of the response, one token at a time.
You'll see periodic progress updates while it's running:

  n_gen  - how many tokens have been generated so far
           (climbs steadily: 100 -> 149 -> 199...)
  tg     - the average generation speed (tokens/sec) across the
           whole task so far
  tg_3s  - a rolling average generation speed over just the last
           3 seconds — useful for spotting a slowdown mid-generation

At the end of the task, a summary is printed:

  eval time = 31885.09 ms / 512 tokens (62.40 ms per token, 16.03 tokens per second)
  total time = 51365.92 ms / 526 tokens

  eval time  - total time spent generating tokens
  total time - prompt processing + generation combined
  n_tokens   - in this final summary, the total token count
               (prompt + generated)

------------------------------------------------------------
WHAT'S "GRAPHS REUSED"?
------------------------------------------------------------

  graphs reused = 509

This is an internal performance optimization. Llama.cpp builds a
"compute graph" describing the math operations needed for each
generation step. Rebuilding this from scratch every token is
wasteful, so the engine reuses a cached graph whenever possible. A
high reuse count is a good sign — it means less overhead per token.

------------------------------------------------------------
SPOTTING PERFORMANCE PROBLEMS
------------------------------------------------------------

The sample log above shows some warning signs worth knowing as a
beginner:

  - Prompt processing at 0.7-0.9 tokens/sec is very slow — a
    GPU-accelerated setup typically processes prompts hundreds of
    times faster.
  - Generation speed of ~16 tokens/sec is on the low end for even a
    small model like Gemma 3 1B.

Both point to the model running on CPU rather than GPU. If your
machine has a compatible graphics card, building llama.cpp with GPU
support (CUDA for NVIDIA, ROCm for AMD, or Vulkan as a cross-vendor
option) can dramatically speed things up.

------------------------------------------------------------
OTHER STARTUP WARNINGS TO KNOW
------------------------------------------------------------

A couple of other lines commonly show up on first run and are worth
understanding rather than ignoring:

  - "CORS is set to allow all origins... no API key is set" — by
    default, the llama.cpp server accepts requests from any website
    and doesn't require authentication. Fine for local
    experimentation, but don't expose this server to the open
    internet without locking it down.

  - "failed to create symlink... switching to degraded mode" — on
    Windows, creating symlinks requires elevated privileges.
    Llama.cpp falls back to copying files instead, which works fine
    but uses more disk space.

  - "server default port will be changed to :9931 in a future
    release" — a heads-up that the default port is changing in an
    upcoming version; if you have scripts hardcoded to port 8080,
    keep an eye on this.

------------------------------------------------------------
SUMMARY
------------------------------------------------------------

  cmn              Common/shared utility log module
  srv              Server module (startup, model loading, networking)
  slot             A worker slot handling one request at a time
  task 0           The ID of a specific inference request
  n_gen            Tokens generated so far in the current task
  tg               Average generation speed (tokens/sec) for the whole task
  tg_3s            Generation speed averaged over the last 3 seconds
  prompt eval time Time spent processing the input prompt
  eval time        Time spent generating the output
  total time       Prompt eval + eval time combined
  n_tokens         Token count (context-dependent: prompt-only or prompt+output)
  graphs reused    Count of cached compute graphs reused (optimization metric)

Once you know how to read these logs, they become a genuinely useful
diagnostic tool — you can tell at a glance whether your setup is
running efficiently, whether it's CPU- or GPU-bound, and how each
request is performing.