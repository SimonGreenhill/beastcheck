class AscertainmentBias(object):
    """Mixin to test for Ascertainment Bias"""
    def test_ascertainment_character(self):
        for seq in self.xml.findall('./data/sequence'):
            site_zero = seq.get('value')[0]
            if site_zero != '0':
                raise AssertionError(
                    "Expected site zero to be 0 for ascertainment"
                )
    
    def test_treeLikelihood_corrects_for_ascertainment(self):
        data = self.xml.find('.//distribution[@id="likelihood"]//data')
        assert data.get('ascertained') == 'true'
        
    def test_treeLikelihood_has_exclude_set_correctly(self):
        data = self.xml.find('.//distribution[@id="likelihood"]//data')
        assert data.get('excludefrom') == '0'
        assert data.get('excludeto') == '1'  # not inclusive.
      
