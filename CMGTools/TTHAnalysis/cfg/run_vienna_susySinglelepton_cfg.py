##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES         ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *

####### Leptons  #####
# lep collection
lepAna.packedCandidates = 'packedPFCandidates'

## ELECTRONS
lepAna.loose_electron_pt  = 5
eleID = "MVAID"

if eleID == "CBID":
  lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
  lepAna.loose_electron_lostHits = 999. # no cut
  lepAna.loose_electron_dxy    = 999.
  lepAna.loose_electron_dz     = 999.

  lepAna.inclusive_electron_id  = ""#"POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
  lepAna.inclusive_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

elif eleID == "MVAID":
  inclusive_electron_id  = "" # same as in susyCore

  #lepAna.loose_electron_id = "POG_MVA_ID_Phys14_NonTrig_VLoose" # Phys14 era
  lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLoose" # Spring15 25ns era

elif eleID == "Incl": # as inclusive as possible
  lepAna.loose_electron_id  = ""
  lepAna.loose_electron_lostHits = 999. # no cut
  lepAna.loose_electron_dxy    = 999.
  lepAna.loose_electron_dz     = 999.

  lepAna.inclusive_electron_id  = ""
  lepAna.inclusive_electron_lostHits = 999.  # no cut
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

## MUONS
lepAna.loose_muon_pt  = 5

# Isolation
isolation = "miniIso"

if isolation == "miniIso":
  # do miniIso
  lepAna.doMiniIsolation = True
  lepAna.miniIsolationPUCorr = 'rhoArea'
  lepAna.miniIsolationVetoLeptons = None
  lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
  lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
  # normal relIso03
  lepAna.ele_isoCorr = "rhoArea"
  lepAna.mu_isoCorr = "rhoArea"

  lepAna.loose_electron_relIso = 0.5
  lepAna.loose_muon_relIso = 0.5


# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 1
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# --- JET-LEPTON CLEANING ---
jetAna.minLepPt = 10
jetAna.applyL2L3Residual = 'Data' 
jetAna.jetPt = 25
jetAna.jetEta = 5.2

jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets =  True #For data

metAna.recalibrate = False #should be false in susycore, already

isoTrackAna.setOff=False
genAna.allGenTaus = True

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHSVAna)

from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheFilterAna = cfg.Analyzer(
    hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False
)

from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer 
LHEAna = LHEAnalyzer.defaultConfig


### Single lepton + ST skim
#from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
#ttHSTSkimmer = cfg.Analyzer(
#    ttHSTSkimmer, name='ttHSTSkimmer',
#    minST = 200,
#    )

#from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer import ttHReclusterJetsAnalyzer
#ttHReclusterJets = cfg.Analyzer(
#    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
#    pTSubJet = 30,
#    etaSubJet = 5.0,
#            )

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import * # central trigger list
from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *
triggerFlagsAna.triggerBits = {
        ## hadronic
        'HT350' : triggers_HT350,
        'HT600' : triggers_HT600,
        'HT800' : triggers_HT800,
        'MET170' : triggers_MET170,
        'HT350MET120' : triggers_HT350MET120,
        'HT350MET100' : triggers_HT350MET100,
        'HTMET' : triggers_HT350MET100 + triggers_HT350MET120,
        ## muon
        'SingleMu' : triggers_1mu,
        'IsoMu27' : triggers_1mu,
        'IsoMu20' : triggers_1mu20,
        'Mu45eta2p1' : trigger_1mu_noiso_r,
        'Mu50' : trigger_1mu_noiso_w,
        'MuHT600' : triggers_mu_ht600,
        'MuHT400MET70' : triggers_mu_ht400_met70,
        'MuHT350MET70' : triggers_mu_ht350_met70,
        'MuHT350MET50' : triggers_mu_ht350_met50,
        'MuHT350' : triggers_mu_ht350,
        'MuHTMET' : triggers_mu_ht350_met70 + triggers_mu_ht400_met70,
        'MuMET120' : triggers_mu_met120,
        'MuHT400B': triggers_mu_ht400_btag,
        ## electrons
        'IsoEle32' : triggers_1el,
        'IsoEle23' : triggers_1el23,
        'IsoEle22' : triggers_1el22,
        'Ele105' : trigger_1el_noiso,
        'EleHT600' : triggers_el_ht600,
        'EleHT400MET70' : triggers_el_ht400_met70,
        'EleHT350MET70' : triggers_el_ht350_met70,
        'EleHT350MET50' : triggers_el_ht350_met50,
        'EleHT350' : triggers_el_ht350,
        'EleHTMET' : triggers_el_ht350_met70 + triggers_el_ht400_met70,
        'EleHT200' :triggers_el_ht200,
        'EleHT400B': triggers_el_ht400_btag,

#mumu
        'mumuIso' : triggers_mumu_iso,
        'mumuNoniso_50ns' : triggers_mumu_noniso_50ns,
        'mumuNoiso' : triggers_mumu_noniso,
        'mumuSS' : triggers_mumu_ss,
        'mumuHT' : triggers_mumu_ht,
# ee
        'ee_DZ': triggers_ee, 
#mue
        'mue':triggers_mue,
#dilepton+HT
        'ee_ht':triggers_ee_ht,
        'mue_ht':triggers_mue_ht,
#multi-lepton
        '3e':triggers_3e,
        '3mu':triggers_3mu,
        '3mu_alt':triggers_3mu_alt,
        '2mu1e':triggers_2mu1e,
        '2e1mu':triggers_2e1mu,
#fake rate
        'FR_1mu_iso':triggers_FR_1mu_iso,
        'FR_1mu_noiso':triggers_FR_1mu_noiso,
        'FR_1e_noiso':triggers_FR_1e_noiso,
        'FR_1e_iso':triggers_FR_1e_iso,
        'FR_1e_b2g':triggers_FR_1e_b2g,
#MET
        'Jet80MET90'       :triggers_Jet80MET90    ,
        'Jet80MET120'      :triggers_Jet80MET120   ,
        'MET120Mu5'        :triggers_MET120Mu5     ,

        'MET170_pres'      :triggers_MET170_pres   , 
        'MET250'           :triggers_MET250        ,
        'MET90nc'          :triggers_MET90nc       ,
        'MET120nc'         :triggers_MET120nc      ,
        'MET90'            :triggers_MET90MHT90    ,
        'MET120'           :triggers_MET120MHT120  ,
        'PhysRates'        :triggers_PhysRate      ,
        'DiPFJetAve100_HFJEC': ["HLT_DiPFJetAve100_HFJEC_v*"],
        'DiPFJetAve140': ["HLT_DiPFJetAve140_v*"],
        'DiPFJetAve160_HFJEC': ["HLT_DiPFJetAve160_HFJEC_v*"],
        'DiPFJetAve200': ["HLT_DiPFJetAve200_v*"],
        'DiPFJetAve220_HFJEC': ["HLT_DiPFJetAve220_HFJEC_v*"],
        'DiPFJetAve260': ["HLT_DiPFJetAve260_v*"],
        'DiPFJetAve300_HFJEC': ["HLT_DiPFJetAve300_HFJEC_v*"],
        'DiPFJetAve320': ["HLT_DiPFJetAve320_v*"],
        'DiPFJetAve40': ["HLT_DiPFJetAve40_v*"],
        'DiPFJetAve400': ["HLT_DiPFJetAve400_v*"],
        'DiPFJetAve500': ["HLT_DiPFJetAve500_v*"],
        'DiPFJetAve60_HFJEC': ["HLT_DiPFJetAve60_HFJEC_v*"],
        'DiPFJetAve60': ["HLT_DiPFJetAve60_v*"],
        'DiPFJetAve80_HFJEC': ["HLT_DiPFJetAve80_HFJEC_v*"],
        'DiPFJetAve80': ["HLT_DiPFJetAve80_v*"],
        }

# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusySingleLepton import *
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusySingleLepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susySingleLepton_globalVariables,
     globalObjects = susySingleLepton_globalObjects,
     collections = susySingleLepton_collections,
)

#!# #-------- SAMPLES AND TRIGGERS -----------

selectedComponents = [
        ]
#susyCoreSequence.insert(-1, hbheFilterAna)
#susyCoreSequence.insert(-1, LHEAna)

sequence = cfg.Sequence(
  susyCoreSequence+
      [ hbheFilterAna, 
        LHEAna,
        ttHEventAna,
        treeProducer,
        ])

isData = False 
#bx = '50ns'
bx = '25ns'

#if True or getHeppyOption("loadSamples"):
if getHeppyOption("loadSamples"):
  from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import *
  if not isData and bx=='50ns':
    selectedComponents = [DYJetsToLL_M50_50ns]
    for comp in selectedComponents:
      comp.files=comp.files[:1]
      comp.splitFactor = 1 
  if not isData and bx=='25ns':
    selectedComponents = [TTJets_DiLepton]
    for comp in selectedComponents:
#      comp.files=['root://xrootd.unl.edu//store/mc/RunIISpring15DR74/tZq_ll_4f_13TeV-amcatnlo-pythia8_TuneCUETP8M1/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v2/40000/102EC100-5D2A-E511-A807-0CC47A4D99A4.root']
      comp.files = comp.files[:1]
      comp.splitFactor = len(comp.files) 
  if isData and bx=='50ns':
    from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
    selectedComponents = [ MuonEG_Run2015B ]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files 
        comp.isMC = False
        comp.isData = True
  if isData and bx=='25ns':
    from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
    selectedComponents = [ DoubleMuon_Run2015D ]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = comp.files[10:11] 
#        comp.files = [ 'root://eoscms.cern.ch//eos/cms/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v3/000/256/676/00000/C2D5A4CC-F55F-E511-A02A-02163E0123FC.root'] 
        comp.isMC = False
        comp.isData = True
#        comp.json = None


#if isData:
#  if bx=='25ns':
#    jecDBFile  = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV5_DATA.db'
#    jecUncFile = 'CondFormats/JetMETObjects/data/Summer15_50nsV5_DATA_UncertaintySources_AK4PFchs.txt'
#    jecEra    = 'Summer15_25nsV5_DATA'
#    mcGT = 'XXX'
#    dataGT= '74X_dataRun2_Prompt_v2' 
#    jetAna.mcGT     = "Summer15_25nsV5_DATA"
#    jetAna.dataGT   = "Summer15_25nsV5_DATA"
#    eventFlagsAna.processName = 'RECO'
#    metAnaDef.metCollection   = ("slimmedMETs","", "RECO") #for PromptReco
#  #  metAnaDef.metCollection   = ("slimmedMETs","", "PAT") #for Jul17 rereco
#  if bx=='50ns':
#    jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_50nsV4_DATA.db'
#    jecUncFile = 'CMGTools/RootTools/data/jec/Summer15_50nsV4_DATA_UncertaintySources_AK4PFchs.txt' 
#    jecEra    = 'Summer15_50nsV4_DATA'
#    mcGT = 'XXX'
#    dataGT= '74X_dataRun2_Prompt_v1' 
#    jetAna.mcGT     = "Summer15_50nsV4_MC"
#    jetAna.dataGT   = "Summer15_50nsV4_DATA"
#    eventFlagsAna.processName = 'RECO'
#    metAnaDef.metCollection   = ("slimmedMETs","", "RECO") #for PromptReco
#  #  metAnaDef.metCollection   = ("slimmedMETs","", "PAT") #for Jul17 rereco
#else: #simulation
#  if bx=='25ns':
#    jecDBFile  = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV2_MC.db'
#    jecUncFile = 'CMGTools/RootTools/data/jec/Summer15_50nsV4_MC_UncertaintySources_AK4PFchs.txt' 
##    jecDBFile = ''
#    jecEra    = 'Summer15_25nsV2_MC' 
#    dataGT= 'XXX' #50ns Data
#    mcGT= 'MCRUN2_74_V9' #25ns MC
#    jetAna.mcGT     = "Summer15_25nsV2_MC"
#    jetAna.dataGT   = "XXX" 
#  if bx=='50ns':
#    jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_50nsV3_MC.db'
#    jecUncFile = 'CMGTools/RootTools/data/jec/Summer15_50nsV4_MC_UncertaintySources_AK4PFchs.txt' 
#    jecEra    = 'Summer15_50nsV3_MC'
#    mcGT= 'MCRUN2_74_V9A' #50ns MC
#    dataGT= 'XXX' #50ns Data
#    jetAna.mcGT     = "Summer15_50nsV3_MC"
#    jetAna.dataGT   = "XXX"#"Summer15_50nsV2"
#
#GT = dataGT if isData else mcGT
#preprocessorFilename = "MetType1_jec_%s_GT_%s_residuals_%s.py"%(jecEra, GT, str(not(removeResiduals)))
#
## -------------------- Running pre-processor
#if getHeppyOption("makePreProcessorFile"): #create preprocessor file on the fly
#  import subprocess
#  extraArgs=[]
#  if isData:
#    extraArgs.append('--isData')
#  if removeResiduals:extraArgs.append('--removeResiduals')
#  preprocessorDir = "$CMSSW_BASE/tmp"
#  preprocessorFile = "/".join([preprocessorDir, preprocessorFilename])
#  args = ['python', 
#    os.path.expandvars('$CMSSW_BASE/python/CMGTools/ObjectStudies/corMETMiniAOD_cfgCreator.py'),\
#    '--GT='+GT, 
#    '--outputFile='+preprocessorFile, 
#    '--jecDBFile='+jecDBFile,
#    '--jecUncFile='+jecUncFile,
#    '--jecEra='+jecEra
#    ] + extraArgs 
#  #print "Making pre-processorfile:"
#  #print " ".join(args)
#  subprocess.call(args)
#else: #use precomputed preprocessor files
#  preprocessorDir = "$CMSSW_BASE/python/CMGTools/TTHAnalysis/preProcFiles"
#  preprocessorFile = "/".join([preprocessorDir, preprocessorFilename])
#
#print "Using preprocessorFile", preprocessorFile
#
#from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
#preprocessor = CmsswPreprocessor(preprocessorFile)

from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
event_class = Events
if getHeppyOption("fetch"):
  event_class = EOSEventsWithDownload

print "Components"
print selectedComponents
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
#                     preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = event_class)

