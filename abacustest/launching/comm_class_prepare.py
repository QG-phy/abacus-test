import traceback
from dp.launching.typing.basic import BaseModel, Int, String, Float, List, Optional, Union, Dict
from dp.launching.typing import (
    BaseModel,
    Set,
    Boolean,
    Field,
    InputFilePath
)
from enum import Enum
from typing import Literal
import re,os,shutil
import dp.launching.typing.addon.ui as ui
from . import comm_class_exampleSource,comm_func

prepare_group = ui.Group("Prepare", "Detail setting for prepare step")


class PPLibEnum(String, Enum):
    dataset1 = "SG15-ONCV-v1_0"

class OrbLibEnum(String, Enum):
    dataset1 = "SG15-Version1_0__StandardOrbitals-Version2_0"

class PPFromDatasets(BaseModel):
    type: Literal["from datasets"]
    dataset: PPLibEnum = Field(title="PP Lib datasets",
                        description="Please choose the PP Lib datasets.")
    dataset_unrecorded: String = Field(default=None,
                                       description="By default, the pp lib \"[SG15-ONCV-v1_0](https://launching.mlops.dp.tech/?request=GET%3A%2Fapplications%2Fabacustest%2Fdatasets%2Fpporb)\" will be used. \
If you want to use other pplib dataset, please enter download link here.")

class OrbFromDatasets(BaseModel):
    type: Literal["from datasets"]
    dataset: OrbLibEnum = Field(title="Orb Lib datasets",
                        description="Please choose the Orb Lib datasets.")
    dataset_unrecorded: String = Field(default=None,
                                       description="By default, the Orb lib \"[SG15-Version1_0__StandardOrbitals-Version2_0](https://launching.mlops.dp.tech/?request=GET%3A%2Fapplications%2Fabacustest%2Fdatasets%2Fpporb)\" will be used. \
If you want to use other pplib dataset, please enter download link here.")


#prepare INPUT template
@prepare_group
class PrepareInputTemplateSet(BaseModel):
    PrepareInputTemplate_local: InputFilePath = Field(default=None,
                                                  title="Upload INPUT template locally",
                                                  description="""You can upload an INPUT file, and then all examples will use the content as INPUT""")
    PrepareInputTemplateSource: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        comm_class_exampleSource.FromDatasets] = Field(title="Prepare INPUT template source",
                              discriminator="type",
                              description="Please choose the INPUT template source.")

#prepare STRU template
@prepare_group
class PrepareStruTemplateSet(BaseModel):
    PrepareStruTemplate_local: InputFilePath = Field(default=None,
                                                  title="Upload STRU template locally",
                                                  description="""You can upload a STRU file, and then all examples will use this structure as STRU""")
    PrepareStruTemplateSource: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        comm_class_exampleSource.FromDatasets] = Field(title="Prepare STRU template source",
                              discriminator="type",
                              description="Please choose the STRU template source.")
        
#prepare KPT template
@prepare_group
class PrepareKptTemplateSet(BaseModel):
    PrepareKptTemplate_local: InputFilePath = Field(default=None,
                                                  title="Upload KPT template locally",
                                                  description="""You can upload a KPT file, and then all examples will use this KPT""")
    PrepareKptTemplateSource: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        comm_class_exampleSource.FromDatasets] = Field(title="Prepare KPT template source",
                              discriminator="type",
                              description="Please choose the KPT template source.")

#prepare dpks descriptor file
@prepare_group
class PrepareDPKSDescriptorSet(BaseModel):
    PrepareDPKSDescriptor_local: InputFilePath = Field(default=None,
                                                  title="Upload DeeP-KS Descriptor locally",
                                                  description="""If you want to use Deep-KS, you can upload the descriptor file here, or prepare the descriptor file in each example directory.""")
    PrepareDPKSDescriptor: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        comm_class_exampleSource.FromDatasets] = Field(title="Prepare DeeP-KS Descriptor source",
                              discriminator="type",
                              description="Please choose the DeeP-KS Descriptor source.") 

#prepare pp lib
@prepare_group
class PreparePPLibSet(BaseModel):
    PreparePPLib_local: InputFilePath = Field(default=None,
                                                  title="Upload pseudopotential library locally",
                                                  description="""If you have a pseudopotential library, you can upload it here. Please also prepare a \"element.json\" file in the library directory, and the key is name of element and value is the name of pseudopotential file.""")
    PreparePPLib: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        PPFromDatasets] = Field(title="Prepare PP Lib source",
                              discriminator="type",
                              description="Please choose the PP Lib source.")   

#prepare ORB lib
@prepare_group
class PrepareOrbLibSet(BaseModel):
    PrepareOrbLib_local: InputFilePath = Field(default=None,
                                                  title="Upload Orbital library locally",
                                                  description="""If you have an Orbital library, you can upload it here. Please also prepare a \"element.json\" file in the library directory, and the key is name of element and value is the name of Orbital file.""")
    PrepareOrbLib: Union[
        comm_class_exampleSource.NotRquired,
        comm_class_exampleSource.FromPreUpload,
        comm_class_exampleSource.FromDatahub,
        OrbFromDatasets] = Field(title="Prepare Orb Lib source",
                              discriminator="type",
                              description="Please choose the Orb Lib source.")    

@prepare_group
class PrepareSet(BaseModel):
    prepare_mix_input: Dict[String,String] = Field(default={},title="Additional INPUT settings",description="You can set additional INPUT parameters for each examples. \
You can set multiple values (separated by comma) for each parameter, which will generate a set of ABACUS inputs for each value. Commonly used parameters: \
\"calculation\", \"ecutwfc\", \"scf_thr\", \"scf_nmax\", \"basis_type\", \"smearing_method\", \"smearing_sigma\", \"mixing_type\", \"mixing_beta\",\"ks_solver\"")
    prepare_mix_kpt: String = Field(default=None,title="Additional KPT settings",description="You can set additional KPT SETTING for each examples. \
Please enter 1/3/6 values seperated by space (such as \"2\" means [2,2,2,0,0,0], which is the 6 value in STRU; \"1 2 3\" means [1,2,3,0,0,0]; \"1 2 3 1 0 0\" means [1,2,3,1,0,0]).\
You can set multiple values (separated by comma), which will generate a set of ABACUS inputs for each value. (Scuch as: \"3, 1 2 3\")")

def parse_prepare_input_stru_kpt_template(templatesource,template_local,work_path, download_path,config,logs,template_name):
    tmp = comm_class_exampleSource.parse_source(templatesource,
                                                template_local,
                                                download_path,
                                                config,
                                                logs)
    if tmp:
        allfiles = os.listdir(download_path)
        if len(allfiles) == 1:
            inputf = allfiles[0]
        elif len(allfiles) > 1 and template_name in allfiles:
            inputf = template_name
        else:
            inputf = None
            logs(f"ERROR: The {template_name} template file is not valid!")
        
        if inputf :
            # copy template file to work_path
            if os.path.isfile(os.path.join(work_path,inputf)):
                os.remove(os.path.join(work_path,inputf))
            os.rename(os.path.join(download_path,inputf),os.path.join(work_path,inputf))
            comm_func.clean_dictorys(download_path)
            return inputf
    return None
    
def parse_prepare(prepare_set,work_path,download_path,logs):
    prepare = {}
    
    # parse INPUT template
    if hasattr(prepare_set,"PrepareInputTemplateSource"):
        input_template = parse_prepare_input_stru_kpt_template(prepare_set.PrepareInputTemplateSource,
                                                               prepare_set.PrepareInputTemplate_local,
                                                               work_path, download_path,
                                                               prepare_set,
                                                               logs,
                                                               "INPUT")
        if input_template:
            prepare["input_template"] = input_template
    
    # parse STRU template
    if hasattr(prepare_set,"PrepareStruTemplateSource"):
        stru_template = parse_prepare_input_stru_kpt_template(prepare_set.PrepareStruTemplateSource,
                                                               prepare_set.PrepareStruTemplate_local,
                                                               work_path, download_path,
                                                               prepare_set,
                                                               logs,
                                                               "STRU")
        if stru_template:
            prepare["stru_template"] = stru_template
    
    # parse KPT template
    if hasattr(prepare_set,"PrepareKptTemplateSource"):
        kpt_template = parse_prepare_input_stru_kpt_template(prepare_set.PrepareKptTemplateSource,
                                                               prepare_set.PrepareKptTemplate_local,
                                                               work_path, download_path,
                                                               prepare_set,
                                                               logs,
                                                               "KPT")
        if kpt_template:
            prepare["kpt_template"] = kpt_template

    
    # parse DPKS descriptor
    if hasattr(prepare_set,"PrepareDPKSDescriptor"):
        dpks_template = parse_prepare_input_stru_kpt_template(prepare_set.PrepareDPKSDescriptor,
                                                              prepare_set.PrepareDPKSDescriptor_local,
                                                              work_path, download_path,
                                                              prepare_set, logs, "jle.orb")
        if dpks_template:
            prepare["dpks_descriptor"] = dpks_template
    
    # parse mix input
    if hasattr(prepare_set,"prepare_mix_input") and prepare_set.prepare_mix_input:
        prepare["mix_input"] = {}
        for key,value in prepare_set.prepare_mix_input.items():
            ivalue = value.split(",")
            prepare["mix_input"][key] = ivalue

    if hasattr(prepare_set,"prepare_mix_kpt") and prepare_set.prepare_mix_kpt:
        kpt_tmp = []
        for ivalue in prepare_set.prepare_mix_kpt.split(","): 
            iivalue = ivalue.split()
            if len(iivalue) == 1:
                try:
                    kpt_tmp.append(int(iivalue[0]))
                except:
                    traceback.print_exc()
                    logs(f"ERROR: The {ivalue} is not valid for KPT!")
            elif len(iivalue) == 3:
                try:
                    kpt_tmp.append([int(iivalue[0]),int(iivalue[1]),int(iivalue[2]),0,0,0])
                except:
                    traceback.print_exc()
                    logs(f"ERROR: The {ivalue} is not valid for KPT!")
            elif len(iivalue) == 6:
                try:
                    kpt_tmp.append([int(iivalue[0]),int(iivalue[1]),int(iivalue[2]),float(iivalue[3]),float(iivalue[4]),float(iivalue[5])])
                except:
                    traceback.print_exc()
                    logs(f"ERROR: The {ivalue} is not valid for KPT!")
            else:
                logs(f"ERROR: The {ivalue} is not valid for KPT!")
                        
        if kpt_tmp:    
            prepare["mix_kpt"] = kpt_tmp
        else:
            logs(f"ERROR: The {prepare_set.prepare_mix_kpt} is not valid for KPT!")
            
    # parse pp lib
    if hasattr(prepare_set,"PreparePPLib"):
        if isinstance(prepare_set.PreparePPLib,PPFromDatasets):
            tmp = None
            try:
                if prepare_set.PreparePPLib.dataset_unrecorded != None and prepare_set.PreparePPLib.dataset_unrecorded.strip() != "":
                    url = prepare_set.PreparePPLib.dataset_unrecorded.strip()
                else:
                    url = comm_class_exampleSource.GetDatasetAddress(prepare_set.PreparePPLib.dataset)
                package = comm_func.download_url(url, download_path)
                if package == None:
                    logs(f"ERROR: download dataset failed!\n\turl:{url}")
                    logs(f"\tPlease check the dataset!")
                else:
                    comm_func.unpack(package, download_path,filetype="tgz")
                    #remove the package
                    os.remove(package)
                    tmp = True
                    #move the package to work_path
            except:
                traceback.print_exc()
        else:
            tmp = comm_class_exampleSource.parse_source(prepare_set.PreparePPLib,prepare_set.PreparePPLib_local,download_path,prepare_set,logs)
        if tmp:
            pp_path = os.path.join(work_path,"pplib")
            if not os.path.isdir(pp_path):
                os.makedirs(pp_path)
            for ifile in os.listdir(download_path):
                shutil.move(os.path.join(download_path,ifile),os.path.join(pp_path,ifile))
            prepare["pp_path"] = "pplib"
        comm_func.clean_dictorys(download_path)
    
    #prepare orb lib
    if hasattr(prepare_set,"PreparePPLib"):
        if isinstance(prepare_set.PrepareOrbLib,OrbFromDatasets):
            tmp = None
            try:
                if prepare_set.PrepareOrbLib.dataset_unrecorded != None and prepare_set.PrepareOrbLib.dataset_unrecorded.strip() != "":
                    url = prepare_set.PrepareOrbLib.dataset_unrecorded.strip()
                else:
                    url = comm_class_exampleSource.GetDatasetAddress(prepare_set.PrepareOrbLib.dataset)
                package = comm_func.download_url(url, download_path)
                if package == None:
                    logs(f"ERROR: download dataset failed!\n\turl:{url}")
                    logs(f"\tPlease check the dataset!")
                else:
                    comm_func.unpack(package, download_path,filetype="tgz")
                    #remove the package
                    os.remove(package)
                    tmp = True
            except:
                traceback.print_exc()
        else:
            tmp = comm_class_exampleSource.parse_source(prepare_set.PrepareOrbLib,prepare_set.PrepareOrbLib_local,download_path,prepare_set,logs)
        if tmp:
            #move the package to work_path
            orb_path = os.path.join(work_path,"orblib")
            if not os.path.isdir(orb_path):
                os.makedirs(orb_path)
            for ifile in os.listdir(download_path):
                shutil.move(os.path.join(download_path,ifile),os.path.join(orb_path,ifile))
            prepare["orb_path"] = "orblib"
        comm_func.clean_dictorys(download_path)
                                                          
    return prepare    
    
def construct_input(datas,opts,work_path,download_path,logs):
    # datas is a dict of examples, created by comm_class_exampleSource.read_source
    #read predft
    need_prepare = False
    logs.iprint("read prepare setting ...")
    prepare = {}

    other_sets = parse_prepare(opts,work_path,download_path,logs)
    if other_sets:
        prepare = other_sets
        need_prepare = True
    
    if datas.get("prepare_example"):
        prepare["example_template"] = datas.get("prepare_example")    
        logs.iprint("\texample:",prepare["example"])
        need_prepare = True
    
    if datas.get("prepare_extrafile"):
        prepare["extra_files"] = datas.get("prepare_extrafile")
        logs.iprint("\tprepare_extrafile:",prepare["extra_files"])
        need_prepare = True
    
    return need_prepare, prepare
    
