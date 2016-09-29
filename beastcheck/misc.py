#!/usr/bin/env python3
#coding=utf-8

class AscertainmentBias(object):
    """Mixin to test for Ascertainment Bias"""
    def test_ascertainment_character(self):
        sequences = self.xml.findall('./data/sequence')
        p = './/distribution[@id="likelihood"]/distribution/data/data'
        for part in self.xml.findall(p):
            try:
                site = int(part.get('filter').split("-")[0])
            except:
                print("Invalid filter %r for %s" % (part.get('filter'), part.get('id')))
                raise

            for seq in sequences:
                site_zero = seq.get('value')[0]
                if site_zero not in ('0', '?', '-'):
                    raise AssertionError(
                        "Expected site zero to be 0/?/- for ascertainment"
                    )

    def test_treeLikelihood_corrects_for_ascertainment(self):
        p = './/distribution[@id="likelihood"]/distribution/data'
        for data in self.xml.findall(p):
            assert data.get('ascertained') == 'true'

    def test_treeLikelihood_has_exclude_set_correctly(self):
        p = './/distribution[@id="likelihood"]/distribution/data'
        for data in self.xml.findall(p):
            # not inclusive
            assert data.get('excludeto') == '1', "%s does not have exclude set to 1" % data.get('id')
