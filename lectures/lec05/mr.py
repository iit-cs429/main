"""
Example using MapReduce to index a collection of documents.

Assumes documents.txt contains one document per line, prefixed with the
document id.

To run: `python mr.py`
"""


import re
from mrjob.job import MRJob


class MRIndexer(MRJob):

    def mapper(self, _, line):
        words = re.findall('\w+', line.lower())
        doc_id = int(words[0])
        for word in set(words[1:]):
            yield word, doc_id

    def reducer(self, key, values):
        #yield key, [v for v in sorted(values)]
        yield key, sorted(values)

if __name__ == '__main__':
    mr_job = MRIndexer(args=['documents.txt'])
    runner = mr_job.make_runner()
    runner.run()
    for line in runner.stream_output():
        key, value = mr_job.parse_output_line(line)
        print key, value
