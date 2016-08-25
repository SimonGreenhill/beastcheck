#!/usr/bin/env python
import os
import re
import sys
import unittest
import subprocess
import xml.etree.ElementTree as ElementTree
from collections import Counter


class IncorrectlyConfigured(Exception):
    pass


class BeastTest(object):
    """Tests a BEAST Analysis"""
    filename = None         # XML Filename
    xml = None              # XML content
    ntaxa = 0               # Number of Taxa
    nchar = 0               # Number of Characters
    ngenerations = 0        # Number of Generations/chainLength
    logEvery = 0            # Log every N generations
    
    # override these if you have specific log file naming
    # that doesn't match filename{.trees,.log}
    tracelog = None
    treelog = None
    
    # validate XML using beast2? 
    validate = False        # do not by default
    beast2 = 'beast2'       # path to beast2
    
    others = {}
    
    @classmethod
    def setUpClass(cls):
        cls.xml = ElementTree.parse(cls.filename)
        
    # helpers
    def get_matching_children(self, entity, pattern, key='id'):
        """
        Searches through children of `entity` returning any that
        have a `key` (default=id) matching the regex in `pattern`.
        """
        pattern = re.compile(pattern)
        # remove entities that don't have this `key` first or we'll try to
        # match pattern on None.
        entities = [e for e in entity.getchildren() if e.get(key) is not None]
        # now match things to pattern
        entities = [e for e in entities if pattern.match(e.get(key))]
        if len(entities) == 0:
            raise IndexError('Unable to find entity match')
        return entities
    
    def _is_in(self, elements, pattern, key='idref'):
        rpattern = re.compile(pattern)
        children = [el.get(key) for el in elements if el.get(key) is not None]
        if len([child for child in children if rpattern.match(child)]):
            return True
        else:
            raise AssertionError("Can't find %s=%s" % (key, pattern))
         
    def is_in_tracelog(self, pattern, key='idref'):
        """Tests that `pattern` is in the tracelog"""
        tracelog = self.xml.find('run/logger[@id="tracelog"]').getchildren()
        return self._is_in(tracelog, pattern, key)
    
    def is_in_operators(self, pattern, key="id"):
        operators = self.xml.findall('.//operator')
        return self._is_in(operators, pattern, key)
    
    def is_in_state(self, pattern, key="id"):
        """Tests that `key`=`pattern` is in the state"""
        state = self.xml.find('./run/state').getchildren()
        return self._is_in(state, pattern, key)
           
    def is_in_prior(self, pattern, key="id"):
        """Tests that `key`=`pattern` is in the state"""
        prior = self.xml.find('./run/distribution/distribution/[@id="prior"]')
        return self._is_in(prior, pattern, key)
    
    # generic tests
    def test_configuration(self):
        """Tests that the BeastTest test case is set up correctly"""
        if not os.path.isfile(self.filename):
            raise IncorrectlyConfigured("Filename does not exist")
        
        try:
            int(self.ntaxa)
        except ValueError:
            raise IncorrectlyConfigured("ntaxa should be an integer")
        
        try:
            int(self.nchar)
        except ValueError:
            raise IncorrectlyConfigured("nchar should be an integer")
        
        try:
            int(self.ngenerations)
        except ValueError:
            raise IncorrectlyConfigured("ngenerations should be an integer")

        try:
            int(self.logEvery)
        except ValueError:
            raise IncorrectlyConfigured("logEvery should be an integer")
    
    def test_others(self):
        for key in sorted(self.others):
            log = self.xml.find('.//*[@id="%s"]' % key)
            assert log is not None, "Cannot find %s" % key
            for attr, expected in self.others[key].items():
                if attr == "_value":
                    assert log.findtext('.') == expected, "%s/%s is not %s" % (
                        key, attr, expected
                    ) 
                else:
                    assert log.get(attr) == expected, "%s/%s is not %s" % (
                        key, attr, expected
                    ) 
    
    def test_ntaxa(self):
        """Tests the number of taxa"""
        taxa = len(self.xml.findall('./data/sequence'))
        if taxa != self.ntaxa:
            e = "Taxa count incorrect (%d != %d)" % (len(taxa), self.ntaxa)
            raise AssertionError(e)
        
    def test_nchar(self):
        """Tests the number of characters"""
        for seq in self.xml.findall('./data/sequence'):
            if len(seq.get('value')) != self.nchar:
                e = "Character Count on %s is not %d" % (
                    seq.get('id'), self.nchar
                )
                raise AssertionError(e)
    
    def test_ngenerations(self):
        """Tests the number of MCMC Generations/ChainLength"""
        gens = int(self.xml.find('run').get('chainLength'))
        if gens != self.ngenerations:
            raise AssertionError("Number of Generations is incorrect")
    
    def test_treelog(self):
        """
        Tests the tree log is named correctly:
            i.e. if filename = x.xml, then x.trees
        """
        if self.treelog is not None:
            expected = self.treelog
        else:
            expected = "%s.trees" % os.path.splitext(self.filename)[0]
        
        treelogs = self.xml.findall('run/logger')
        if expected not in [f.get('fileName') for f in treelogs]:
            raise AssertionError("Expected Tree log to be %s" % expected)

    def test_tracelog(self):
        """
        Tests the trace log is named correctly:
            i.e. if filename = x.xml, then x.log
        """
        if self.tracelog is not None:
            expected = self.tracelog
        else:
            expected = "%s.log" % os.path.splitext(self.filename)[0]
        
        log = self.xml.find('run/logger[@id="tracelog"]')
        
        if log is None:
            raise AssertionError("No tracelog defined")
        if log.get('fileName') != expected:
            raise AssertionError("Expected Trace log to be %s" % expected)
    
    def test_logEvery_tracelog(self):
        log = self.xml.find('run/logger[@id="tracelog"]')
        if int(log.get('logEvery')) != self.logEvery:
            raise AssertionError(
                "Tracelog is not logging every %d" % self.logEvery
            )

    def test_logEvery_treelog(self):
        loggers = self.xml.findall('run/logger')
        loggers = [l for l in loggers if l.get('mode') == 'tree']
        for log in loggers:
            if int(log.get('logEvery')) != self.logEvery:
                raise AssertionError(
                    "Treelog is not logging every %d" % self.logEvery
                )
    
    def test_for_duplicate_ids(self):
        idlist = Counter([x.get('id') for x in self.xml.iter() if x.get('id')])
        duplicates = [i for i in idlist if idlist[i] > 1]
        if len(duplicates):
            raise ValueError("Duplicate IDs in XML: %r" % duplicates)
    
    # helper for testing calibrations
    def check_calibration(self, clade, members, log=True, monophyletic=True):
        
        if log:  # check logging
            self.is_in_tracelog(clade)
        
        # check in prior
        prior = self.xml.find('./run/distribution/distribution/[@id="prior"]')
        try:
            cal = self.get_matching_children(prior, clade)[0]
        except IndexError:
            raise IndexError("Unable to find %s in prior" % clade)
        
        # check monophyletic
        if monophyletic:
            assert cal.get('monophyletic') == 'true'
        else:
            assert cal.get('monophyletic') in ('false', None)
        
        taxa = []
        for t in cal[0].findall('.//taxon'):
            if t.get('id'):
                taxa.append(t.get('id'))
            else:
                taxa.append(t.get('idref'))
        self.assertEqual(sorted(members), sorted(taxa))
    
    def test_xml(self):
        if not self.validate:
            return True
            
        try:
            with open(os.devnull, 'w') as null:
                rv = subprocess.check_call(
                    [self.beast2, '-validate', self.filename],
                    stdout=null, stderr=subprocess.STDOUT
                )
        except subprocess.CalledProcessError:
            raise ValueError("beast couldn't validate the XML")
    


