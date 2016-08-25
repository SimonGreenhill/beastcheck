#!/usr/bin/env python3
#coding=utf-8

# Clock Models
import re

class StrictClock(object):
    """Mixin to test clock model"""
    def test_treelikelihood_has_strict_BranchRateModel(self):
        spec = "beast.evolution.branchratemodel.StrictClockModel"
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, 'treeLikelihood\..*')[0]
        brm = treelh.find("branchRateModel")
        assert brm is not None, "No branchRateModel in treeLikelihood"
        assert brm.get('id').startswith('StrictClock.c')
        assert brm.get('spec') == spec, 'spec mismatch'
    
    # state
    def test_state_clockRate(self):
        assert self.is_in_state("clockRate\.c:.*")
    
    # priors
    def test_prior_ClockPrior(self):
        assert self.is_in_prior('ClockPrior\.c:.*')
    
    # operators
    def test_operator_StrictClockRateScaler(self):
        assert self.is_in_operators("StrictClockRateScaler\.c.*")
    
    def test_operator_strictClockUpDownOperator(self):
        assert self.is_in_operators("strictClockUpDownOperator\.c.*")
    
    # logging
    def test_tracelog_ucldMean(self):
        assert self.is_in_tracelog('clockRate\.c:.*')
    
    def test_tree_has_correct_branchrates(self):
        treelogs = self.xml.findall('run/logger[@mode="tree"]')
        for treelog in treelogs:
            brm = treelog.find('log').get('branchratemodel')
            # is this correct?
            assert brm is None, 'check the branchratemodel'
        


class RelaxedClock(object):
    """Mixin to test clock model"""
    def test_treelikelihood_has_relaxed_BranchRateModel(self):
        spec = "beast.evolution.branchratemodel.UCRelaxedClockModel"
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, 'treeLikelihood\..*')[0]
        brm = treelh.find("branchRateModel")
        assert brm is not None, "No branchRateModel in treeLikelihood"
        assert brm.get('id').startswith('RelaxedClock.c')
        assert brm.get('spec') == spec, 'spec mismatch'
    
    # state
    def test_state_ucldStdev(self):
        assert self.is_in_state("ucldStdev\.c:.*")
    
    def test_state_ucldMean(self):
        assert self.is_in_state("ucldMean\.c:.*")
    
    def test_state_rateCategories(self):
        assert self.is_in_state("rateCategories\.c:.*")
    
    def test_state_rateCategories_dimension(self):
        """
        Checks that the number of dimensions in the rateCategories is equal to:
            (2 * ntaxa) - 2
        """
        p = re.compile(r"""rateCategories\.c:.*""")
        state = self.xml.find('./run/state')
        children = [
            s for s in state.getchildren() if p.match(s.get('id', 'No'))
        ]
        if len(children) == 0:
            raise AssertionError("Unable to find rateCategories.c in state")
        elif len(children) > 1:
            raise AssertionError("Multiple rateCategories.c in state")
        
        dimension = int(children[0].get('dimension'))
        expected = (self.ntaxa * 2) - 2
        if dimension != expected:
            raise AssertionError(
                'Dimension is %d not %d' % (expected, dimension)
            )
    
    # priors
    def test_prior_ucldStdevPrior(self):
        assert self.is_in_prior('ucldStdevPrior\.c:.*')
        
    # operators
    def test_operator_ucldMeanScaler(self):
        assert self.is_in_operators("ucldMeanScaler\.c.*")
    
    def test_operator_ucldStdevScaler(self):
        assert self.is_in_operators("ucldStdevScaler\.c.*")
    
    def test_operator_CategoriesRandomWalk(self):
        assert self.is_in_operators("CategoriesRandomWalk\.c.*")
    
    def test_operator_CategoriesSwapOperator(self):
        assert self.is_in_operators("CategoriesSwapOperator\.c.*")
    
    def test_operator_CategoriesUniform(self):
        assert self.is_in_operators("CategoriesUniform\.c.*")
    
    def test_operator_relaxedUpDownOperator(self):
        assert self.is_in_operators("relaxedUpDownOperator\.c.*")
    
    # logging
    def test_tracelog_ucldMean(self):
        assert self.is_in_tracelog('ucldMean\.c:.*')
    
    def test_tracelog_ucldStdev(self):
        assert self.is_in_tracelog('ucldStdev\.c:.*')
 
    def test_tracelog_rate_c(self):
        assert self.is_in_tracelog('rate\.c:.*', key='id')
    
    def test_tree_has_correct_branchrates(self):
        treelogs = self.xml.findall('run/logger[@mode="tree"]')
        for treelog in treelogs:
            brm = treelog.find('log').get('branchratemodel')
            if brm is None:
                raise AssertionError("Expected a branchratemodel")
                assert brm.startswith("@RelaxedClock.c"), "Expected a RelaxedClock branchratemodel"
