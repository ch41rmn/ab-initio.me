---
layout: post
title:  "Welcome to Jekyll!"
date:   2021-07-18 16:38:15 +1000
categories: jekyll
description: |
  Lessons in using Jekyll for the first time - Github actions, Jekyll favicon, and SEO
---
This blog is built by Jekyll, which is a tool that allows software engineers who writes markdown documentation during work to also blog using markdown at night and on the weekends.

And GitHub Pages' support for Jekyll is almost perfect. Almost.

Time for a few quick lessons learned then.

## Do I need GitHub actions?
I thought I needed GitHub actions to build the Jekyll site... it turns out I didn't. It's *automagic*.

This was a pleasant surprise, but also slightly annoying. In my day job as a developer, I try to minimise side effects in my applications, especially if the they are not explicitly requested (Zen of python: explicit is better than implicit). This definitely falls in the camp of implicit side effects.

But upon further thought, this is actually rather reasonable.
- With the very helpful guide at [[1]](#ref1), I was able to get the action `helaili/jekyll-action@v2` running without too much fuss.
- The build job looks like it's installing lots of ruby and jekyll dependencies, and takes a full 5 minutes to do so.
- While this is not a heavy workload, imagine if this action is repeated for every user on every push.
- GitHub Pages' automatic compilation clocks in at mere seconds, presumably using a shared build service for everybody's blogs. This is much better for Microsoft's wallet, and also better for the polar bears.

## What if I want the "this is fine" dog as a favicon?
This turned out to be surprisingly tedious.

The first results from Google for "jekyll add favicon" are:
- a Medium article
- an unknown domain that has a "how-to"-esque title
- a bunch of StackOverflow threads
- noticeably missing are any official pages from [jekyllrb.com](jekyllrb.com) on this topic.

Feeling unsupported, I did what any developer would do: open 5 StackOverflow threads. These threads are all variations of the same advice to add `<link rel="icon">` elements into the page header, which is fine except that I have no idea where the headers are defined.

I then applied another typical link-prioritisation method: skip the Medium article and click on Google result #2 [[2]](#ref2). This took me to a small personal blog, also written in Jekyll, where I learned that the responsibility of favicons lies firmly with theme developers. I then began getting flashbacks from the golden days of messing with Wordpress themes.

The instructions were ultimately helpful though, despite being rather verbose. Here is an abridged version for a time-poor engineer who wants a blog in a rush:
- Create an `_includes/` folder in this jekyll site, anything in here will override the corresponding theme file.
- Find the path to the theme, via `bundle info minima` or whichever theme we are now overriding.
- In there is a file that manages the `<head>` section for the theme, such as `${theme_path}/_includes/head.html` or `${theme_path}/_includes/head/custom.html`.
- Copy it to the same relative location in this jekyll site, and modify to our heart's content, such as adding all the `<link rel="icon">` elements.

And for that, we get to have this:

<center><img src="/favicon-32x32.png"/></center>

## That's nice, but I don't have a Jekyll blog. How can I find this post in the future?

I googled this blog, "ab initio blog", and the results are ego-crushingly unrelated, only helped by the fact that my domain has only existed for 3 hours.

I then googled "github pages seo", and an official Github blog post from 2016 appeared at result #3 [[3]](#ref3). It told me I can simply add `{% raw %}{% raw %}{% seo %}{%{% endraw %} endraw %}` to the header template, and then GitHub will tell Google to put me on the front page for absolutely everything. This is neat, as we just created an override for that.

Upon looking, the header already has `{% raw %}{%- seo -%}{% endraw %}`. The difference then, I assume, might be due to improvements in the Jekyll syntax since 2016.

All this means though, it is again *automagic*. So in a few days when I search for "ab initio blog" again, I may have to think of another excuse as to why my domain doesn't appear.

Or worse, I may have to actually learn the dark arts of SEO.

EDIT:

While trying to render the `{% raw %}{% raw %}...{%{% endraw %} endraw %}` code snippet during the writing of this post, they started disappearing into the void. It turns out they are are escape blocks for rendering Jekyll templating code in Jekyll. Perhaps it's not changes in the Jekyll language then, but that the Github author thought he was writing Jekyll when it was really just Vanilla Markdown...

FWIW, to render the code snippet correctly, the escape sequence looks like this: `{% raw %}{% raw %}{% raw %}{% seo %}{%{%{% endraw %} endraw %} endraw %}`.

The escape sequence used to render the escape sequence above is left as a reader exercise.


## References

1. <a name="ref1" href="https://jekyllrb.com/docs/continuous-integration/github-actions/">https://jekyllrb.com/docs/continuous-integration/github-actions/</a>
2. <a name="ref2" href="https://ptc-it.de/add-favicon-to-mm-jekyll-site/">https://ptc-it.de/add-favicon-to-mm-jekyll-site/</a>
3. <a name="ref3" href="https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/">https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/</a>
