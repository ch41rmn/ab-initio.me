---
layout:     post
title:      "Migrating a Chia Farm to a Pi"
date:       2021-09-06 22:56:53 +10:00
categories: pi storage chia crypto
description: |
  Some instructions on setting up a Pi to farm Chia
---

Yes yes, I have finally given in to crypto. I won't try to defend myself.

So this shall just be some technical notes for setting up Chia
farming on a Raspberry Pi or ROCK Pi device.

## Notes on plotting

- Use the MadMax plotter [[1]](#ref-chia-plotter-by-madmax)
- Don't plot on a Pi. It doesn't have nearly enough memory and CPU, and we haven't
  even touched the topic of disk throughput.
- Don't plot on WSL.
  - Maybe it'll work for you, but it failed badly for me.
  - WSL runs on HyperV under the hood (at least in my case it did)
  - Plotting is an intense exercise, it will push CPU/memory/disk to the limits
  - When plotting on WSL, the entire ubuntu VM can crash, causing you to lose the entire plot
- Use PowerShell (if you're on Windows)
  ```
  # contract address is 62 characters (0-9a-z)
  # get this from Chia GUI -> Pool -> ? beside pool name
  # or via CLI, `chia plotnft show`
  $CONTRACT_ADDRESS = "xch..."

  # farmer public key is 96 characters (hex)
  # get this from Chia GUI -> Keys -> eye
  # or via CLI, `chia keys show`
  $FARMER_PUB_KEY = ""

  $THREADS = 4  # match cpu cores
  $THREADx = 1  # 2 if hyperthreading

  $PLOTS = 27   # match disk size

  # replace this with path to mad-max-plotter binary
  ..\local\chia-plotter-win-v0.1.6\chia_plot.exe `
    --size 32 `
    --count $PLOTS `
    --threads $THREADS `
    --rmulti2 $THREADx `
    --tmpdir tmpdir/ `
    --tmpdir2 tmpdir2/ `
    --finaldir destination/ `
    --farmerkey $FARMER_PUB_KEY `
    --contract $CONTRACT_ADDRESS `
    2>&1 | % ToString | Tee-Object -FilePath output.txt -Append
  ```

## Notes on farmer setup

Prerequisites:
- Run the Chia GUI on a more powerful machine (plotting computer?)
- Wait for a fully sync'd node + wallet
- Join a pool and wait until confirmation

Farmer setup:
- Recommended:
  - Ensure you have some swap space (4-8GB), and plenty of disk space (30+GB)
  - Create a `chia` user with its own home directory, no password, and definitely no sudo privileges
- Follow standard ubuntu installation instructions [[2]](#ref-chia-blockchain-ubuntu-installation)
- DO NOT RUN `chia start <>` YET
- Run `chia init`, and `chia keys add` to setup the new client
- From the full node machine, copy the blockchain db to the Farmer
  - `~/.chia/mainnet/db`, ~15GB at the time of writing
  - `~/.chia/mainnet/wallet/db`, ~5GB at the time of writing
  - SFTP is nice here, if you have WSL already
  - See below on the gotcha
- Copy the above db directories into corresponding folders in the farmer
- On the farmer, modify `~/.chia/mainnet/config/config.yaml`. In jsonpath syntax:
  - `$.farmer.logging.log_level`: set to `INFO` if you want a log of when partials are submitted to pools
  - `$.pool.pool_list[0]`: copy the pool list config from the config file on the full node machine
  - `$.harvester.plot_directories`: add the list of directories containing plots
- Now, you can run `chia start farmer`
  - After a few minutes, the following should show that the farmer node is running and healthy
  - `chia show -s`: Full Node Synced
  - `chia wallet show`: Wallet Synced
  - `chia plotnft show`: Wallet is farming to the pool, and the pool URL is as expected
- Setup systemd so that chia starts automatically when the Pi restarts
  - In `/etc/systemd/system/chia-farmer.service`:
    ```
    [Unit]
    Description=Chia Farmer
    Wants=network-online.target
    After=network.target network-online.target
    StartLimitIntervalSec=0
    [Service]
    Type=forking
    Restart=always
    RestartSec=1
    User=chia
    Environment=PATH=/home/chia/chia-blockchain/venv/bin:${PATH}
    ExecStart=/usr/bin/env chia start farmer -r
    ExecStop=/usr/bin/env chia stop all -d
    [Install]
    WantedBy=multi-user.target
    ```
  - `sudo systemctl daemon-reload`
  - `sudo systemctl enable chia-farmer`


# Gotcha - What if I don't copy the blockchain db?

If you choose to not do this, the Pi will struggle a LOT trying to sync the blocks.

Symptoms:
- Full node sync will take a couple of days
- Wallet sync will be stuck at block height 0
- Pi will constantly run out of memory and hang

Running `chia start farmer-no-wallet` will alleviate some OOM and hanging issues.
However the farmer won't be submitting partials, as partials submission appears
to require the full `plotnft` information, which in turn depends on a working wallet.

A few people have reported different aspects of this problem, this post is the collation of the
suggested resolutions to get things to work. [[3]](#ref-pool-farming-problem-report-1) [[4]](#ref-pool-farming-problem-report-2) [[5]](#ref-pool-farming-problem-report-3)

# References

1. chia-plotter by MadMax: <a name="ref-chia-plotter-by-madmax" href="https://github.com/madMAx43v3r/chia-plotter">https://github.com/madMAx43v3r/chia-plotter</a>
1. chia-blockchain Ubuntu installation: <a name="ref-chia-blockchain-ubuntu-installation" href="https://github.com/Chia-Network/chia-blockchain/wiki/INSTALL#ubuntudebian">https://github.com/Chia-Network/chia-blockchain/wiki/INSTALL#ubuntudebian</a>
1. Pool farming problem report 1: <a name="ref-pool-farming-problem-report-1" href="https://chiaforum.com/t/pool-farming-without-wallet-sync-not-working/10770">https://chiaforum.com/t/pool-farming-without-wallet-sync-not-working/10770</a>
1. Pool farming problem report 2: <a name="ref-pool-farming-problem-report-2" href="https://chiaforum.com/t/points-not-updating/10149/11">https://chiaforum.com/t/points-not-updating/10149/11</a>
1. Pool farming problem report 3: <a name="ref-pool-farming-problem-report-3" href="https://github.com/Chia-Network/chia-blockchain/issues/7210">https://github.com/Chia-Network/chia-blockchain/issues/7210</a>
