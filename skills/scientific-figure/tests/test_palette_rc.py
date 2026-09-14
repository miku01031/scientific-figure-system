from src.palette_api import resolve
import pytest
@pytest.mark.parametrize('name',['our_moderate_vivid'])
def test_registry_explicit(name):assert len(resolve({'palette':name},['A','B','C'])['colors'])==3
def test_default_legacy():assert resolve({},['A']) is None
@pytest.mark.parametrize('family',['default'])
def test_auto_family(family):assert resolve({'palette':'auto','palette_family':family},['A','B'])
def test_high_contrast_capacity():
 with pytest.raises(ValueError,match='UNKNOWN_CATEGORICAL_PALETTE'):resolve({'palette':'tol_high_contrast'},['A','B','C','D'])
def test_unknown_closed():
 with pytest.raises(ValueError):resolve({'palette':'rainbow'},['A'])
def test_semantic_invariance():assert resolve({'palette':'our_moderate_vivid'},['A'])['semantic_colors']==resolve({'palette':'our_moderate_vivid'},['A'])['semantic_colors']
def test_focus():
 r=resolve({'color_strategy':'focus_context','focus_identity':'B'},['A','B','C']);assert r['colors']['A']==r['colors']['C']!=r['colors']['B']
 with pytest.raises(ValueError):resolve({'color_strategy':'focus_context'},['A'])
def test_contrast_qa():assert resolve({'palette':'our_moderate_vivid'},list('ABCDEF'),'line')['warnings']
