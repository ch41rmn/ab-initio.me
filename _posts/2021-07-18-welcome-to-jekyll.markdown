---
layout: post
title:  "Welcome to Jekyll!"
date:   2021-07-18 16:38:15 +1000
categories: jekyll
description: |
  Lessons in using Jekyll for the first time - Github actions, Jekyll favicon, and SEO
---
GitHub Pages' support for Jekyll is almost perfect. Almost.

Time for a few quick lessons learned then.

## Do I need GitHub actions?
I thought I needed GitHub actions to build the Jekyll site... it turns out I didn't. It's *automagic*.

This was a pleasant surprise, but also slightly annoying. In my day job as a developer, I try to minimise side effects in my applications, especially if the they are not explicitly requested (Zen of python: explicit is better than implicit). This definitely falls in the camp of implicit side effect.

But upon further thought, this is actually rather reasonable.
- With the very helpful guide at [[1]](#ref1), I was able to get the action `helaili/jekyll-action@v2` running quite quickly, even though it was ultimately unnecessary.
- The build job looks like it's installing lots of ruby and jekyll dependencies, and takes a full 5 minutes to do so.
- While this is not a heavy workload, imagine if this action is repeated for every user on every push.
- GitHub Pages' automatic compilation clocks in at mere seconds, presumably using a shared build service for everybody's blogs. This is much better for Microsoft's wallet, and also better for the polar bears.

## What if I want the "this is fine" dog as a favicon?
This turned out to be surprisingly tedious.

The first results from Google for "jekyll add favicon" are:
- a Medium article
- an unknown domain that has a "how-to"-esque title
- a bunch of StackOverflow threads.
- Noticeably missing are any official pages on [jekyllrb.com](jekyllrb.com) about this topic.

Feeling unsupported, I did what any developer would do: open 5 StackOverflow threads. These threads all mentioned I need to add some `<link rel="icon">` elements into the page header, which is fine except that I don't know where the headers are defined.

I then applied another typical link-prioritisation method: skip the Medium article and click on Google result #2 [[2]](#ref2). This took me to a small personal blog, also written in Jekyll, where I learned that the responsibility of favicons lies firmly with theme developers, and I began getting flashbacks from the golden days of messing with Wordpress themes.

The instructions were ultimately helpful though, despite being rather long. Here is an abridged version for a time-poor engineer who wants to read less and code more:
- Create an `_includes/` folder in this jekyll site, anything in here will override the corresponding theme file
- Find the path to the theme, via `bundle info minima` or whichever theme we are now overriding
- In there is a file that manages the `<head>` section for the theme, such as `${theme_path}/_includes/head.html` or `${theme_path}/_includes/head/custom.html`
- Copy it to the same relative location in this jekyll site, and modify to our heart's content, such as adding all the `<link rel="icon">` elements.

<center><img src="/favicon-32x32.png"/></center>

## That's nice, but I don't have a Jekyll blog. How can I find this answer in the future?

I googled this blog, "ab initio blog". The results are definitely ego-crushing, only helped by the fact that the domain has only existed for 3 hours.

I then googled "github pages seo", and an official Github blog post from 2016 appeared at result #3 [[3]](#ref3).
- It told me I can simply add `{% raw %}{% seo %}{% endraw %}` to the header template.
- This is neat, as we just created an override for that.
- The header already had `{%- seo -%}`. The difference, I assume, is due to 2016 being the technology equivalent of the dark ages when compared to 2021.

Which means, in a few days when I search for "ab initio blog" again, I may have to think of another excuse as to why my domain doesn't appear.

Or worse, I may have to actually learn the dark arts of SEO.

## References

1. <a name="ref1" href="https://jekyllrb.com/docs/continuous-integration/github-actions/">https://jekyllrb.com/docs/continuous-integration/github-actions/</a>
2. <a name="ref2" href="https://ptc-it.de/add-favicon-to-mm-jekyll-site/">https://ptc-it.de/add-favicon-to-mm-jekyll-site/</a>
3. <a name="ref3" href="https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/">https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/</a>
