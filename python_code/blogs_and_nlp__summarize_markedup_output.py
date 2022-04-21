# -*- coding: utf-8 -*-

import os
import sys
import json
import nltk
import numpy
from blogs_and_nlp__summarize import summarize

HTML_TEMPLATE = """<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    </head>
    <body>%s</body>
</html>"""

if __name__ == '__main__':

    # Load in output from blogs_and_nlp__get_feed.py

    BLOG_DATA = sys.argv[1]
    blog_data = json.loads(open(BLOG_DATA).read())

    # Marked up version can be written out to disk

    if not os.path.isdir('out/summarize'):
        os.makedirs('out/summarize')

    for post in blog_data:
       
        post.update(summarize(post['content']))

        # You could also store a version of the full post with key sentences markedup
        # for analysis with simple string replacement...

        for summary_type in ['top_n_summary', 'mean_scored_summary']:
            post[f'{summary_type}_marked_up'] = f"<p>{post['content']}</p>"
            for s in post[summary_type]:
                post[f'{summary_type}_marked_up'] = post[
                    f'{summary_type}_marked_up'
                ].replace(s, f'<strong>{s}</strong>')


            filename = post['title'] + '.summary.' + summary_type + '.html'
            with open(os.path.join('out', 'summarize', filename), 'w') as f:
                html = HTML_TEMPLATE % (
                    post['title'] + ' Summary',
                    post[f'{summary_type}_marked_up'],
                )

                f.write(html.encode('utf-8'))
            print >> sys.stderr, "Data written to", f.name
