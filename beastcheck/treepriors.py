#!/usr/bin/env python3
#coding=utf-8


class YuleTreePrior(object):
    
    def test_yule_state_birthRate(self):
        assert self.is_in_state("birthRate\.t:.*")
        
    def test_yule_prior_YuleModel(self):
        assert self.is_in_prior("YuleModel\.t:.*")
        
    def test_yule_prior_YuleBirthRatePrior(self):
        assert self.is_in_prior("YuleBirthRatePrior\.t:.*")
    
    def test_yule_operators(self):
        assert self.is_in_operators("YuleBirthRateScaler\.t:.*")
        assert self.is_in_operators("YuleModelTreeScaler\.t:.*")
        assert self.is_in_operators("YuleModelTreeRootScaler\.t:.*")
        assert self.is_in_operators("YuleModelUniformOperator\.t:.*")
        assert self.is_in_operators("YuleModelSubtreeSlide\.t:.*")
        assert self.is_in_operators("YuleModelNarrow\.t:.*")
        assert self.is_in_operators("YuleModelWide\.t:.*")
        assert self.is_in_operators("YuleModelWilsonBalding\.t:.*")
        
    def test_yule_logging(self):
        assert self.is_in_tracelog("YuleModel\.t:.*")
        assert self.is_in_tracelog("birthRate\.t:.*")


class CalibratedYuleTreePrior(object):
    
    def test_yule_state_birthRateY(self):
        assert self.is_in_state("birthRateY\.t:.*")
        
    def test_yule_prior_CalibratedYuleModel(self):
        assert self.is_in_prior("CalibratedYuleModel\.t:.*")
        
    def test_yule_prior_CalibratedYuleBirthRatePrior(self):
        assert self.is_in_prior("CalibratedYuleBirthRatePrior\.t:.*")
    
    def test_yule_operators(self):
        assert self.is_in_operators("CalibratedYuleModelTreeScaler\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelTreeRootScaler\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelUniformOperator\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelSubtreeSlide\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelNarrow\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelWide\.t:.*")
        assert self.is_in_operators("CalibratedYuleModelWilsonBalding\.t:.*")
        assert self.is_in_operators("CalibratedYuleBirthRateScaler\.t:.*")
    
    def test_yule_logging(self):
        assert self.is_in_tracelog("CalibratedYuleModel\.t:.*")
        assert self.is_in_tracelog("birthRateY\.t:.*")
    
    # TODO: other checks -- all calibrations must be monophyletic
    # TODO: other checks -- all calibrations must have a distribution


class BayesianSkylineTreePrior(object):
    
    def test_BSP_state_bPopSizes(self):
        assert self.is_in_state('bPopSizes\.t:.*')

    def test_BSP_state_bGroupSizes(self):
        assert self.is_in_state('bGroupSizes\.t:.*')
    
    def test_BSP_prior_MarkovChainedPopSizes(self):
        assert self.is_in_prior('MarkovChainedPopSizes\.t:.*')
    
    def test_BSP_prior_BayesianSkyline(self):
        assert self.is_in_prior('BayesianSkyline\.t:.*')

    def test_BSP_operators(self):
        assert self.is_in_operators("BayesianSkylineTreeScaler\.t:.*")
        assert self.is_in_operators("BayesianSkylineTreeRootScaler\.t:.*")
        assert self.is_in_operators("BayesianSkylineUniformOperator\.t:.*")
        assert self.is_in_operators("BayesianSkylineSubtreeSlide\.t:.*")
        assert self.is_in_operators("BayesianSkylineNarrow\.t:.*")
        assert self.is_in_operators("BayesianSkylineWide\.t:.*")
        assert self.is_in_operators("BayesianSkylineWilsonBalding\.t:.*")
        assert self.is_in_operators("popSizesScaler\.t:.*")
        assert self.is_in_operators("groupSizesDelta\.t:.*")
    
    def test_BSP_logging(self):
        assert self.is_in_tracelog("BayesianSkyline\.t:.*")
        assert self.is_in_tracelog("bPopSizes\.t:.*")
        assert self.is_in_tracelog("bGroupSizes\.t:.*")
        

class BirthDeathSkylineSerialTreePrior(object):
    
    def test_BDSS_state_origin(self):
        assert self.is_in_state("origin\.t:.*")
    
    def test_BDSS_state_rho(self):
        assert self.is_in_state("rho\.t:.*")
    
    def test_BDSS_state_becomeUninfectiousRate(self):
        assert self.is_in_state("becomeUninfectiousRate\.t:.*")
    
    def test_BDSS_state_R0(self):
        assert self.is_in_state("R0")
    
    def test_BDSS_prior_BirthDeathSkySerial(self):
        assert self.is_in_prior('BirthDeathSkySerial\.t:.*')
        
    def test_BDSS_prior_becomeUninfectiousRatePrior(self):
        assert self.is_in_prior('becomeUninfectiousRatePrior\.t:.*')

    def test_BDSS_prior_originPrior(self):
        assert self.is_in_prior('originPrior\.t:.*')

    def test_BDSS_prior_rhoPrior(self):
        assert self.is_in_prior('rhoPrior\.t:.*')

    def test_BDSS_prior_R0_Prior(self):
        assert self.is_in_prior('R0_Prior')
    
    def test_BDSS_operators(self):
        assert self.is_in_operators("becomeUninfectiousRateScaler\.t:.*")
        assert self.is_in_operators("rhoScaler\.t:.*")
        assert self.is_in_operators("origScaler\.t:.*")
        assert self.is_in_operators('R0_scaler')
        assert self.is_in_operators("BDSKY_serial_treeScaler\.t:.*")
        assert self.is_in_operators("BDSKY_serial_treeRootScaler\.t:.*")
        assert self.is_in_operators("BDSKY_serial_UniformOperator\.t:.*")
        assert self.is_in_operators("BDSKY_serial_SubtreeSlide\.t:.*")
        assert self.is_in_operators("BDSKY_serial_narrow\.t:.*")
        assert self.is_in_operators("BDSKY_serial_wide\.t:.*")
        assert self.is_in_operators("BDSKY_serial_WilsonBalding\.t:.*")
        
    def test_BDSS_logging(self):
        assert self.is_in_tracelog("BirthDeathSkySerial\.t:.*")
        assert self.is_in_tracelog("origin\.t:.*")
        assert self.is_in_tracelog("rho\.t:.*")
        assert self.is_in_tracelog("becomeUninfectiousRate\.t:.*")
        assert self.is_in_tracelog("R0")