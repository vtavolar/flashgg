import FWCore.ParameterSet.Config as cms
from flashgg.MicroAOD.flashggPrunedGenParticles_cfi import flashggPrunedGenParticles
from flashgg.MicroAOD.flashggGenPhotons_cfi import flashggGenPhotons
from flashgg.MicroAOD.flashggGenBquarks_cfi import flashggGenBquarks
from flashgg.MicroAOD.flashggGenPhotonsExtra_cfi import flashggGenPhotonsExtra

from flashgg.MicroAOD.flashggGenLeptons_cfi import flashggGenLeptons
from flashgg.MicroAOD.flashggGenLeptonsExtra_cfi import flashggGenLeptonsExtra
from flashgg.MicroAOD.flashggGenJetsExtra_cfi import flashggGenJetsExtra


flashggMicroAODGenSequence = cms.Sequence(flashggPrunedGenParticles+flashggGenPhotons*flashggGenPhotonsExtra + flashggGenLeptons*flashggGenLeptonsExtra + flashggGenJetsExtra + flashggGenBquarks
                                        )
