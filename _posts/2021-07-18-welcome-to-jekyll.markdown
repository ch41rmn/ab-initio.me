---
layout: post
title:  "Welcome to Jekyll!"
date:   2021-07-18 16:38:15 +1000
categories: jekyll
description: |
  Lessons in using Jekyll for the first time - Github actions, Jekyll favicon, and SEO
---
This blog is built by Jekyll, which is a tool that allows software engineers who write documentation using markdown at work to also write blogs using markdown at night and on the weekend.

And GitHub Pages' support for Jekyll is almost perfect. Almost.

Time for a few quick lessons learned then.

## What is Jekyll? And GitHub pages?

Jekyll [[1]](#ref-jekyll) is a ruby web development/templating tool, that can render markdown with various power-ups into a static html site. It also has built-in support for basic themes.

GitHub Pages [[2]](#ref-github-pages) is a free "hosting" service, which serves simple static websites directly out of a GitHub repository. It also has built-in support for Jekyll and custom domain names. It even takes care of the SSL certificate if you use a custom domain name.

This combination is really quite nice:
- Free (except domain name registration)
- Write content in markdown, inside a git repository
- Off-the-shelf themes, no need to worry about the look-and-feel
- No server-side resources to manage, just a static html site hosted with GitHub
- No more excuses such as "my Wordpress got hacked because I didn't keep up with patching, and now I don't want a blog for the next 5 years"

## Do I need GitHub actions?
I thought I needed GitHub actions to build the Jekyll site into the actual html site... it turns out I didn't. It's *automagic*.

This was a pleasant surprise, but also slightly annoying. In my day job as a developer, I try to minimise side effects in my applications, especially if the they are not explicitly requested (Zen of python: explicit is better than implicit). This feels like an implicit side effect.

But upon further thought, this is rather reasonable.
- With the very helpful guide at [[3]](#ref-jekyll-action), I was able to get the action `helaili/jekyll-action@v2` running without too much fuss.
- The build job has to install ruby and jekyll dependencies on a bare ubuntu container, and takes a full 5 minutes to do so.
- While this is not a heavy workload, imagine if this action is repeated for every user on every push.
- GitHub Pages' automatic compilation clocks in at mere seconds, presumably using a shared build service for everybody's blogs. This is much better for Microsoft's wallet, and also better for the polar bears.

## What if I want the "this is fine" dog as a favicon?
This turned out to be surprisingly tedious.

The first results from Google for "jekyll add favicon" are:
- a Medium article
- an unknown domain that has a "how-to"-esque title
- a bunch of StackOverflow threads
- noticeably missing are any official pages from [jekyllrb.com](#ref-jekyll) on this topic.

Feeling unsupported, I did what any developer would do: open 5 StackOverflow threads. These threads are all variations of the same advice to add `<link rel="icon">` elements into the page header, which is fine except that I have no idea where the headers are defined.

I then applied another typical link-prioritisation method: skip the Medium article and click on Google result #2 [[4]](#ref-favicon). This took me to a small personal blog, also written in Jekyll, where I learned that the responsibility of favicons lies firmly with theme developers. I then began getting flashbacks from the golden days of messing with Wordpress themes.

The instructions were ultimately helpful, despite being verbose. Here is an abridged version for a time-poor engineer who wants a new blog in a rush:
- Create an `_includes/` folder in this jekyll site, anything in here will override the corresponding theme file.
- Find the path to the theme, via `bundle info minima` or whichever theme we are now overriding.
- In there is a file that manages the `<head>` section for the theme, such as `${theme_path}/_includes/head.html` or `${theme_path}/_includes/head/custom.html`.
- Copy it to the same relative location in this jekyll site, and modify to our heart's content, such as adding all the `<link rel="icon">` elements.

And for all that, we get to have this:

<center><img src="/favicon-32x32.png"/></center>

## That's nice, but I don't have a Jekyll blog. How can I find this post in the future?

I googled this blog, the "ab initio blog". The results are ego-crushingly unrelated, only helped by the fact that this domain has only existed for 3 hours.

I then googled "github pages seo", and an official Github blog post from 2016 appeared at result #3 [[4]](#ref4). It told me I can simply add `{% raw %}{% raw %}{% seo %}{%{% endraw %} endraw %}` to the header template. GitHub will then tell Google to put me on the front page for absolutely everything. This is neat, as we just learned how to add things into the header.

It turns out my header already has `{% raw %}{%- seo -%}{% endraw %}`. The difference, I assume, might be due to improvements in the Jekyll syntax since 2016.

It is again *automagic* then. So in a few days when I search for "ab initio blog" again, I may have to think of another excuse as to why my domain doesn't appear.

Or worse, I may have to learn the dark arts of SEO.

EDIT:

While trying to render the code snippet for `{% raw %}{% raw %}...{%{% endraw %} endraw %}`, they started disappearing into the void. It turns out they are escape blocks for rendering Jekyll templating code in Jekyll. Perhaps the Github blog author thought he should be writing Jekyll, when it was really just Vanilla Markdown...

FWIW, to render the code snippet correctly, the escape sequence looks like this: `{% raw %}{% raw %}{% raw %}...{%{%{% endraw %} endraw %} endraw %}`.

The escape sequence used to render the escape sequence is left as a reader exercise.


## References

1. Jekyll: <a name="ref-jekyll" href="https://jekyllrb.com">https://jekyllrb.com</a>
1. GitHub Pages: <a name="ref-github-pages" href="https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages">https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages</a>
1. Jekyll docs on GitHub Actions: <a name="ref-jekyll-action" href="https://jekyllrb.com/docs/continuous-integration/github-actions/">https://jekyllrb.com/docs/continuous-integration/github-actions/</a>
1. Blog post on adding favicon to Jekyll site: <a name="ref-favicon" href="https://ptc-it.de/add-favicon-to-mm-jekyll-site/">https://ptc-it.de/add-favicon-to-mm-jekyll-site/</a>
1. GitHub blog on SEO for GitHub pages: <a name="ref-seo" href="https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/">https://github.blog/2016-05-10-better-discoverability-for-github-pages-sites/</a>
