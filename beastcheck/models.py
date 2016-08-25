#!/usr/bin/env python3
#coding=utf-8


class ModelCTMC(object):
    """Tests CTMC Analyses"""
    def test_userdatatype(self):
        """Test CTMC userDataType"""
        udt = self.xml.find('./data/userDataType')
        assert udt.get('spec') == "beast.evolution.datatype.StandardData"
        assert udt.get('ambiguities') == ""
        assert int(udt.get('nrOfStates')) == 2
        
    def test_siteModel_is_GeneralSubstitutionModel(self):
        """
        siteModel should have a substModel of class GeneralSubstitutionModel
        """
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'GeneralSubstitutionModel'
    
    def test_substModel_rates(self):
        """substModel should have a rates parameter"""
        substModel = self.xml.find('.//substModel')
        rates = self.get_matching_children(substModel, "rates\.s:.*")
        assert len(rates) == 1, "Unable to find rates parameter"
        assert int(rates[0].get('dimension')) == 2
    
    def test_substModel_frequency(self):
        """
        Tests that substModel has a frequencies parameter
        """
        substModel = self.xml.find('.//substModel')
        freqs = self.get_matching_children(
            substModel, "Frequencies", key="spec"
        )
        assert len(freqs) == 1, 'Unable to Find Frequencies Parameter'
    
    def test_frequencies_estimated(self):
        """Frequencies are estimated"""
        # fragile?
        assert self.is_in_operators("FrequenciesExchanger\.s:.*")
        

class ModelCovarion(object):
    """Tests Covarion Analyses"""
    def test_state_bcov_alpha(self):
        """bcov_alpha should be in the state"""
        assert self.is_in_state('bcov_alpha\.s:.*')
    
    def test_state_bcov_s(self):
        """bcov_s should be in the state"""
        assert self.is_in_state('bcov_s\.s:.*')
    
    def test_substModel(self):
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'BinaryCovarion'
        assert substModel.get('alpha').startswith('@bcov_alpha.s')
        assert substModel.get('hfrequencies').startswith('@hiddenfrequencies')
        assert substModel.get('vfrequencies').startswith('@frequencies.s')
        assert substModel.get('switchRate').startswith('@bcov_s.s')
    
    def test_useAmbiguities_is_true(self):
        """Covarion needs ambiguity in the likelihood"""
        lh = self.xml.find('.//distribution[@id="likelihood"]')
        treelh = self.get_matching_children(lh, 'treeLikelihood\..*')
        if treelh[0].get('useAmbiguities') != 'true':
            raise AssertionError('Covarion needs ambiguity')
    
    def test_prior_bcov_alpha(self):
        assert self.is_in_prior('bcov_alpha_prior\.s:.*')
    
    def test_prior_bcov_s(self):
        assert self.is_in_prior('bcov_s_prior\.s:.*')
    
    def test_frequencies_estimated(self):
        """Frequencies are estimated"""
        # fragile?
        assert self.is_in_operators("frequenciesDelta\.s:.*")
    
    def test_hfrequencies_estimated(self):
        """Hidden frequencies are estimated"""
        # fragile?
        assert self.is_in_operators("hFrequenciesDelta\.s:.*")
    
    def test_operator_bcovAlphaScaler(self):
        assert self.is_in_operators("bcovAlphaScaler\.s:.*")
    
    def test_operator_bcovSwitchParamScaler(self):
        assert self.is_in_operators("bcovSwitchParamScaler\.s:.*")
    
    def test_tracelog_bcov_alpha(self):
        assert self.is_in_tracelog('bcov_alpha\.s:.*')
    
    def test_tracelog_bcov_s(self):
        assert self.is_in_tracelog('bcov_s\.s:.*')
    
    def test_tracelog_frequencies(self):
        assert self.is_in_tracelog('frequencies\.s:.*')
    
    def test_tracelog_hiddenfrequencies(self):
        assert self.is_in_tracelog('hiddenfrequencies\.s:.*')
    
    
class ModelGamma(object):
    """Tests Models with Gamma Distributed Rate Heterogeneity"""
    def test_state_gammaShape(self):
        """gammaShape should be in state"""
        assert self.is_in_state('gammaShape.s')
    
    def test_prior_gammaShape(self):
        assert self.is_in_prior('GammaShapePrior\.s:.*')
    
    def test_siteModel_gammaCategoryCount_gt_1(self):
        """Site model should have GammaCategoryCount > 1"""
        siteModel = self.xml.find('.//siteModel')
        try:
            gammaCategoryCount = int(siteModel.get('gammaCategoryCount'))
        except TypeError:
            raise TypeError("No gammaCategoryCount on siteModel")
        
        if gammaCategoryCount <= 1:
            raise ValueError("GammaCategoryCount is %d" % gammaCategoryCount)
    
    def test_siteModel_has_gammaShape(self):
        siteModel = self.xml.find('.//siteModel')
        assert siteModel.get('shape') is not None, "No gammaShape on siteModel"
    
    def test_operator_gammaShapeScaler(self):
        """gammaShapeScaler should be in operators"""
        assert self.is_in_operators("gammaShapeScaler\..*")
    
    def test_tracelog_gammaShape(self):
        assert self.is_in_tracelog('gammaShape\.*')
     
        
class ModelDollo(object):
    """Tests Dollo Analyses"""
    
    # data
    def test_userdatatype_not_in_data(self):
        assert self.xml.find('./data/userDataType') is None
    
    def test_userdatatype(self):
        """Test Dollo userDataType"""
        udt = self.xml.find('.//userDataType')
        assert udt.get('spec') == "beast.evolution.datatype.UserDataType"
        assert udt.get('codeMap') is not None
        assert int(udt.get('states')) == 4
        assert int(udt.get('codelength')) == 1
    
    # state
    def test_state_clockRate(self):
        assert self.is_in_state("cognateDeathRate\.s:.*", key='idref')
    
    # substModel
    def test_substModel_is_MutationDeathModel(self):
        substModel = self.xml.find('.//substModel')
        if substModel is None:
            raise IndexError("substModel not found")
        assert substModel.get('spec') == 'MutationDeathModel'
    
    def test_substModel_frequency(self):
        """
        Tests that substModel has a frequencies parameter
        """
        substModel = self.xml.find('.//substModel')
        freqs = self.get_matching_children(
            substModel, "Frequencies", key="spec"
        )
        assert len(freqs) == 1, 'Unable to Find Frequencies Parameter'
    
    def test_substModel_deathprob(self):
        """
        Tests that substModel has a deathprob parameter
        """
        substModel = self.xml.find('.//substModel')
        params = self.get_matching_children(
            substModel, "cognateDeathRate", key="id"
        )
        assert len(params) == 1, 'Unable to find deathprob'
    
    # operators
    def test_operator_cognateDeathRateOperator(self):
        assert self.is_in_operators("cognateDeathRateOperator\.s.*")
    
    # logging
    def test_tracelog_cognateDeathRate(self):
        assert self.is_in_tracelog('cognateDeathRate\.s:.*')
    



