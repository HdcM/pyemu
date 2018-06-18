import os
if not os.path.exists("temp"):
    os.mkdir("temp")


def from_io_with_inschek_test():
    import os
    from pyemu import Pst,pst_utils
    # creation functionality
    dir = os.path.join("..","verification","10par_xsec","template_mac")
    pst = Pst(os.path.join(dir,"pest.pst"))


    tpl_files = [os.path.join(dir,f) for f in pst.template_files]
    out_files = [os.path.join(dir,f) for f in pst.output_files]
    ins_files = [os.path.join(dir,f) for f in pst.instruction_files]
    in_files = [os.path.join(dir,f) for f in pst.input_files]


    new_pst = Pst.from_io_files(tpl_files, in_files,
                                ins_files, out_files,
                                pst_filename=os.path.join("temp","test.pst"))
    print(new_pst.observation_data)
    return

def tpl_ins_test():
    import os
    from pyemu import Pst,pst_utils
    # creation functionality
    dir = os.path.join("..","verification","henry","misc")
    files = os.listdir(dir)
    tpl_files,ins_files = [],[]
    for f in files:
        if f.lower().endswith(".tpl") and "coarse" not in f:
            tpl_files.append(os.path.join(dir,f))
        if f.lower().endswith(".ins"):
            ins_files.append(os.path.join(dir,f))

    out_files = [f.replace(".ins",".junk") for f in ins_files]
    in_files = [f.replace(".tpl",".junk") for f in tpl_files]

    pst_utils.pst_from_io_files(tpl_files, in_files,
                                ins_files, out_files,
                                pst_filename=os.path.join("temp","test.pst"))
    return


def res_test():
    import os
    import numpy as np
    from pyemu import Pst,pst_utils
    # residual functionality testing
    pst_dir = os.path.join("pst")

    p = Pst(os.path.join(pst_dir,"pest.pst"))
    phi_comp = p.phi_components
    assert "regul_p" in phi_comp
    assert "regul_m" in phi_comp

    p.adjust_weights_resfile()

    d = np.abs(p.phi - p.nnz_obs)
    assert d < 1.0E-5
    p.adjust_weights(obsgrp_dict={"head": 50})
    assert np.abs(p.phi_components["head"] - 50) < 1.0e-6

    # get()
    new_p = p.get()
    new_p.prior_information = p.prior_information
    new_file = os.path.join("temp", "new.pst")
    new_p.write(new_file)

    p_load = Pst(new_file,resfile=p.resfile)
    for gname in p.phi_components:
        d = np.abs(p.phi_components[gname] - p_load.phi_components[gname])
        assert d < 1.0e-5

def pst_manip_test():
    import os
    from pyemu import Pst
    pst_dir = os.path.join("pst")
    org_path = os.path.join(pst_dir,"pest.pst")
    new_path = os.path.join("temp","pest1.pst")
    pst = Pst(org_path)
    pst.control_data.pestmode = "regularisation"
    pst.write(new_path)
    pst = Pst(new_path)
    pst.svd_data.maxsing = 1
    pst.write(new_path,update_regul=True)


def load_test():
    import os
    from pyemu import Pst,pst_utils
    pst_dir = os.path.join("pst")
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    # just testing all sorts of different pst files
    pst_files = os.listdir(pst_dir)
    exceptions = []
    load_fails = []
    for pst_file in pst_files:
        if pst_file.endswith(".pst") and not "comments" in pst_file and \
                not "missing" in pst_file:
            print(pst_file)
            try:
                p = Pst(os.path.join(pst_dir,pst_file))
            except Exception as e:
                exceptions.append(pst_file + " read fail: " + str(e))
                load_fails.append(pst_file)
                continue
            out_name = os.path.join(temp_dir,pst_file)
            print(out_name)
           #p.write(out_name,update_regul=True)
            try:
                p.write(out_name,update_regul=True)
            except Exception as e:
                exceptions.append(pst_file + " write fail: " + str(e))
                continue
            print(pst_file)
            try:
                p = Pst(out_name)
            except Exception as e:
                exceptions.append(pst_file + " reload fail: " + str(e))
                continue

    #with open("load_fails.txt",'w') as f:
    #    [f.write(pst_file+'\n') for pst_file in load_fails]
    if len(exceptions) > 0:
        raise Exception('\n'.join(exceptions))


def flex_load_test():
    import os
    from pyemu import Pst,pst_utils
    pst_dir = os.path.join("pst")
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    # just testing all sorts of different pst files
    pst_files = os.listdir(pst_dir)
    exceptions = []
    load_fails = []
    for pst_file in pst_files:
        if pst_file.endswith(".pst") and not "missing" in pst_file:
            #if not pst_file.startswith("LPR"):
            #    continue
            print(pst_file)
            p = Pst(os.path.join(pst_dir, pst_file), flex=True)
            out_name = os.path.join(temp_dir, pst_file)
            print("write")
            p.write(out_name, update_regul=True)
            p = Pst(out_name)
           #  try:
           #      p = Pst(os.path.join(pst_dir,pst_file),flex=True)
           #  except Exception as e:
           #      exceptions.append(pst_file + " read fail: " + str(e))
           #      load_fails.append(pst_file)
           #      continue
           #  out_name = os.path.join(temp_dir,pst_file)
           #  print(out_name)
           # #p.write(out_name,update_regul=True)
           #  try:
           #      p.write(out_name,update_regul=True)
           #  except Exception as e:
           #      exceptions.append(pst_file + " write fail: " + str(e))
           #      continue
           #  print(pst_file)
           #  try:
           #      p = Pst(out_name)
           #  except Exception as e:
           #      exceptions.append(pst_file + " reload fail: " + str(e))
           #      continue

    #with open("load_fails.txt",'w') as f:
    #    [f.write(pst_file+'\n') for pst_file in load_fails]
    if len(exceptions) > 0:
        raise Exception('\n'.join(exceptions))

def comments_test():

    import os
    import pyemu


    pst = pyemu.Pst(os.path.join("pst","comments.pst"))
    pst.with_comments = True
    pst.write(os.path.join("temp","comments.pst"))
    pst1 = pyemu.Pst(os.path.join("temp","comments.pst"))
    assert pst1.parameter_data.extra.dropna().shape[0] == pst.parameter_data.extra.dropna().shape[0]
    pst1.with_comments = False
    pst1.write(os.path.join("temp","comments.pst"))
    pst2 = pyemu.Pst(os.path.join("temp","comments.pst"))
    assert pst2.parameter_data.dropna().shape[0] == 0

def smp_test():
    import os
    from pyemu.pst.pst_utils import smp_to_dataframe,dataframe_to_smp,\
        parse_ins_file,smp_to_ins
    
    smp_filename = os.path.join("misc","gainloss.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))

    smp_filename = os.path.join("misc","sim_hds_v6.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))


def smp_dateparser_test():
    import os
    from pyemu.pst.pst_utils import smp_to_dataframe,dataframe_to_smp,\
        parse_ins_file,smp_to_ins

    smp_filename = os.path.join("misc","gainloss.smp")
    df = smp_to_dataframe(smp_filename,datetime_format= "%d/%m/%Y %H:%M:%S")
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))

    smp_filename = os.path.join("misc","sim_hds_v6.smp")
    df = smp_to_dataframe(smp_filename)
    print(df.dtypes)
    dataframe_to_smp(df,smp_filename+".test")
    smp_to_ins(smp_filename)
    obs_names = parse_ins_file(smp_filename+".ins")
    print(len(obs_names))


def tied_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    print(pst.tied)
    pst.write(os.path.join("temp","pest_tied_tester_1.pst"))
    mc = pyemu.MonteCarlo(pst=pst)
    mc.draw(1)
    mc.write_psts(os.path.join("temp","tiedtest_"))

    par = pst.parameter_data
    par.loc[pst.par_names[::3],"partrans"] = "tied"
    try:
        pst.write(os.path.join("temp", "pest_tied_tester_1.pst"))
    except:
        pass
    else:
        raise Exception()
    par.loc[pst.par_names[::3],"partied"] = pst.par_names[0]

    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    print(pst.tied)
    par = pst.parameter_data
    par.loc[pst.par_names[2],"partrans"] = "tied"
    print(pst.tied)
    par.loc[pst.par_names[2],"partied"] = "junk1"
    pst.write(os.path.join("temp","test.pst"))
    pst = pyemu.Pst(os.path.join("temp","test.pst"))

    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    print(pst.tied)
    par = pst.parameter_data
    par.loc[pst.par_names[2], "partrans"] = "tied"
    par.loc[pst.par_names[2],"partied"] = "junk"
    pst.write(os.path.join("temp", "test.pst"))
    pst = pyemu.Pst(os.path.join("temp", "test.pst"))


def derivative_increment_tests():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","inctest.pst"))
    pst.calculate_pertubations()


def pestpp_args_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    pst.pestpp_options["lambdas"] = "0.1,0.2,0.3"
    pst.write(os.path.join("temp","temp.pst"))
    pst = pyemu.Pst(os.path.join("temp","temp.pst"))
    print(pst.pestpp_options)


def reweight_test():
    import os
    import numpy as np
    from pyemu import Pst,pst_utils
    pst_dir = os.path.join("pst")
    p = Pst(os.path.join(pst_dir,"pest.pst"))
    obsgrp_dict = {"pred":1.0,"head":1.0,"conc":1.0}
    p.adjust_weights(obsgrp_dict=obsgrp_dict)
    assert np.abs(p.phi - 3.0) < 1.0e-5,p.phi

    obs = p.observation_data
    obs.loc[obs.obgnme=="pred","weight"] = 0.0
    assert np.abs(p.phi - 2.0) < 1.0e-5,p.phi

    obs_dict = {"pd_one":1.0,"pd_ten":1.0}
    p.adjust_weights(obs_dict=obs_dict)
    assert np.abs(p.phi - 4.0) < 1.0e-5,p.phi


def reweight_res_test():
    import os
    import numpy as np
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    print(pst.res.loc[pst.nnz_obs_names,:])
    print(pst.phi,pst.nnz_obs)
    pst.adjust_weights_resfile()
    print(pst.phi,pst.nnz_obs)
    assert np.abs(pst.phi - pst.nnz_obs) < 1.0e-6


def regul_rectify_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","inctest.pst"))
    pyemu.helpers.zero_order_tikhonov(pst)
    assert pst.prior_information.shape[0] == pst.npar_adj
    pst._update_control_section()
    assert pst.control_data.nprior == pst.prior_information.shape[0]
    fix_names = pst.adj_par_names[::2]
    pst.parameter_data.loc[fix_names,"partrans"] = "fixed"
    pst.rectify_pi()
    assert pst.prior_information.shape[0] == pst.npar_adj
    pst._update_control_section()
    assert pst.control_data.nprior == pst.prior_information.shape[0]


def nnz_groups_test():
    import os
    import pyemu
    pst_dir = os.path.join("pst")
    pst = pyemu.Pst(os.path.join(pst_dir,"br_opt_no_zero_weighted.pst"))
    org_og = pst.obs_groups
    org_nnz_og = pst.nnz_obs_groups
    obs = pst.observation_data
    obs.loc[obs.obgnme==org_og[0],"weight"] = 0.0
    new_og = pst.obs_groups
    new_nnz_og = pst.nnz_obs_groups
    assert org_og[0] not in new_nnz_og


def regdata_test():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    phimlim = 10.0
    pst.reg_data.phimlim = phimlim
    pst.control_data.pestmode = "regularization"
    pst.write(os.path.join("temp","pest_regultest.pst"))
    pst_new = pyemu.Pst(os.path.join("temp","pest_regultest.pst"))
    assert pst_new.reg_data.phimlim == phimlim


def plot_flopy_par_ensemble_test():
    import shutil
    import numpy as np
    try:
        import flopy
    except:
        return
    try:
        import matplotlib.pyplot as plt
    except:
        print("error importing pyplot")
        return
    try:
        import shapely
    except:
        print("error importing shapely")
        return

    import pyemu
    bd = os.getcwd()
    try:
        org_model_ws = os.path.join("..", "examples", "Freyberg_transient")
        nam_file = "freyberg.nam"

        new_model_ws = "temp_pst_from_flopy"
        pp_props = [["upw.hk", 0], ["upw.hk", 1]]
        helper = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws, org_model_ws,
                                                 grid_props=pp_props, remove_existing=True,
                                                 model_exe_name="mfnwt")

        pst = pyemu.Pst(os.path.join(new_model_ws,"freyberg.pst"))
        mc = pyemu.MonteCarlo(pst=pst)
        os.chdir(new_model_ws)
        cov = pyemu.Cov.from_ascii("freyberg.pst.prior.cov")
        mc.draw(100,cov=cov)
        #pyemu.helpers.plot_flopy_par_ensemble(mc.pst, mc.parensemble, num_reals=None, model=helper.m)
        #pyemu.helpers.plot_flopy_par_ensemble(mc.pst, mc.parensemble, num_reals=None)

        import cartopy.crs as ccrs
        import cartopy.io.img_tiles as cimgt

        import pyproj
        # except:
        #     return

        stamen_terrain = cimgt.StamenTerrain()
        zoom = 10

        def fig_ax_gen():
            fig = plt.figure(figsize=(20,20))
            nrow,ncol = 5,4

            axes = []
            for i in range(nrow*ncol):
                #print(i)
                ax = plt.subplot(nrow,ncol,i+1,projection=stamen_terrain.crs)
                ax.set_extent([-97.775, -97.625, 30.2, 30.35])
                #ax.set_extent([175.2, 176.2, -37, -38.2])
                ax.add_image(stamen_terrain,zoom)
                #plt.show()
                axes.append(ax)

                #break
            return fig, axes
        #fig,axes = fig_ax_gen()
        #plt.show()
        #return
        pcolormesh_trans = ccrs.UTM(zone=14)
        pyemu.helpers.plot_flopy_par_ensemble(mc.pst, mc.parensemble, num_reals=None,fig_axes_generator=fig_ax_gen,
                                              pcolormesh_transform=pcolormesh_trans,model="freyberg.nam")

        os.chdir("..")
    except Exception as e:
        os.chdir(bd)
        raise Exception(str(e))

def from_flopy_kl_test():
    import shutil
    import numpy as np
    import pandas as pd
    try:
        import flopy
    except:
        return
    import pyemu
    org_model_ws = os.path.join("..", "examples", "freyberg_sfr_update")
    nam_file = "freyberg.nam"
    m = flopy.modflow.Modflow.load(nam_file, model_ws=org_model_ws, check=False)
    flopy.modflow.ModflowRiv(m, stress_period_data={0: [[0, 0, 0, 30.0, 1.0, 25.0],
                                                        [0, 0, 1, 31.0, 1.0, 25.0],
                                                        [0, 0, 1, 31.0, 1.0, 25.0]]})
    hfb_data = []
    jcol1, jcol2 = 14, 15
    for i in range(m.nrow):
        hfb_data.append([0, i, jcol1, i, jcol2, 0.001])
    flopy.modflow.ModflowHfb(m, 0, 0, len(hfb_data), hfb_data=hfb_data)

    org_model_ws = "temp"
    m.change_model_ws(org_model_ws)
    m.write_input()

    new_model_ws = "temp_pst_from_flopy"

    hds_kperk = []
    for k in range(m.nlay):
        for kper in range(m.nper):
            hds_kperk.append([kper, k])
    temp_bc_props = [["wel.flux", None]]
    spat_bc_props = [["riv.cond", 0], ["riv.stage", 0]]
    kl_props = [["upw.hk",0],["upw.vka",0],["rch.rech",0]]
    ph = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws=new_model_ws,
                                         org_model_ws=org_model_ws,
                                         kl_props=kl_props,
                                         remove_existing=True,
                                         model_exe_name="mfnwt")


def from_flopy():

    import shutil
    import numpy as np
    import pandas as pd
    try:
        import flopy
    except:
        return
    import pyemu

    org_model_ws = os.path.join("..","examples","freyberg_sfr_update")
    nam_file = "freyberg.nam"
    m = flopy.modflow.Modflow.load(nam_file, model_ws=org_model_ws, check=False)
    flopy.modflow.ModflowRiv(m,stress_period_data={0:[[0,0,0,30.0,1.0,25.0],
                                                      [0,0,1,31.0,1.0,25.0],
                                                      [0,0,1,31.0,1.0,25.0]]})
    hfb_data = []
    jcol1, jcol2 = 14, 15
    for i in range(m.nrow):
        hfb_data.append([0, i, jcol1, i, jcol2, 0.001])
    flopy.modflow.ModflowHfb(m, 0, 0, len(hfb_data), hfb_data=hfb_data)

    org_model_ws = "temp"
    m.change_model_ws(org_model_ws)
    m.write_input()

    new_model_ws = "temp_pst_from_flopy"

    hds_kperk = []
    for k in range(m.nlay):
        for kper in range(m.nper):
            hds_kperk.append([kper, k])
    temp_bc_props = [["wel.flux",None]]
    spat_bc_props = [["riv.cond", 0], ["riv.stage", 0]]
    ph = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws=new_model_ws,
                                         org_model_ws=org_model_ws,
                                         zone_props=[["rch.rech", 0], ["rch.rech", [1, 2]]],
                                         remove_existing=True,
                                         model_exe_name="mfnwt",temporal_bc_props=temp_bc_props,
                                         spatial_bc_props=spat_bc_props,hfb_pars=True)


    par = ph.pst.parameter_data
    pe = ph.draw(100)

    par.loc["welflux_000",'parval1'] = 2.0

    os.chdir(new_model_ws)
    ph.pst.write_input_files()
    pyemu.helpers.apply_bc_pars()
    os.chdir("..")



    ph = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws=new_model_ws,
                                         org_model_ws=org_model_ws,
                                         zone_props=[["rch.rech", 0], ["rch.rech", [1, 2]]],
                                         remove_existing=True,
                                         model_exe_name="mfnwt",
                                         spatial_bc_props=spat_bc_props)
    pe = ph.draw(100)

    ph = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws=new_model_ws,
                                         org_model_ws=org_model_ws,
                                         zone_props=[["rch.rech", 0], ["rch.rech", [1, 2]]],
                                         remove_existing=True,
                                         model_exe_name="mfnwt", temporal_bc_props=temp_bc_props)
    pe = ph.draw(100)
    ph.pst.parameter_data.loc["rech0_zn1", "parval1"] = 2.0

    bd = os.getcwd()
    os.chdir(new_model_ws)
    # try:
    ph.pst.write_input_files()
    csv = os.path.join("arr_pars.csv")
    df = pd.read_csv(csv)
    df.loc[:,"upper_bound"] = np.NaN
    df.loc[:,"lower_bound"] = np.NaN
    df.to_csv(csv)
    pyemu.helpers.apply_array_pars()

    df.loc[:, "org_file"] = df.org_file.iloc[0]
    df.loc[:, "model_file"] = df.org_file
    df.loc[:, "upper_bound"] = np.arange(df.shape[0])
    df.loc[:, "lower_bound"] = np.NaN
    print(df)
    df.to_csv(csv)
    try:
        pyemu.helpers.apply_array_pars()
    except:
        pass
    else:
        raise Exception()
    df.loc[:, "lower_bound"] = np.arange(df.shape[0])
    df.loc[:, "upper_bound"] = np.NaN
    print(df)
    df.to_csv(csv)
    try:
        pyemu.helpers.apply_array_pars()
    except:
        pass
    else:
        raise Exception()

    df.loc[:, "lower_bound"] = 0.1
    df.loc[:, "upper_bound"] = 0.9
    print(df)
    df.to_csv(csv)

    pyemu.helpers.apply_array_pars()
    arr = np.loadtxt(df.model_file.iloc[0])
    assert arr.min() >= df.lower_bound.iloc[0]
    assert arr.max() <= df.upper_bound.iloc[0]

    # except:
    #     pass
    os.chdir(bd)

    org_model_ws = os.path.join("..", "examples", "freyberg_sfr_update")
    nam_file = "freyberg.nam"
    m = flopy.modflow.Modflow.load(nam_file, model_ws=org_model_ws, check=False)

    helper = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws, org_model_ws,
                                             hds_kperk=[0, 0], remove_existing=True,
                                             model_exe_name="mfnwt", sfr_pars=True, sfr_obs=True)
    pe = helper.draw(100)
    bd = os.getcwd()

    pp_props = [["upw.ss",[0,1]],["upw.ss",1],["upw.ss",2],["extra.prsity",0],\
                ["rch.rech",0],["rch.rech",[1,2]]]
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,new_model_ws,org_model_ws,
                                    pp_props=pp_props,hds_kperk=[0,0],remove_existing=True,
                                             model_exe_name="mfnwt")

    m = flopy.modflow.Modflow.load(nam_file,model_ws=org_model_ws,exe_name="mfnwt",check=False)
    const_props = [["rch.rech",i] for i in range(m.nper)]
    helper = pyemu.helpers.PstFromFlopyModel(m,new_model_ws,
                                    const_props=const_props,hds_kperk=[0,0],remove_existing=True)
    pe = helper.draw(100)
    grid_props = [["extra.pr",0]]
    for k in range(3):
        #grid scale pars for hk in all layers
        grid_props.append(["upw.hk",k])
        # const par for hk, ss, sy in all layers
        const_props.append(["upw.hk",k])
        const_props.append(["upw.ss",k])
        const_props.append(["upw.sy",k])
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,new_model_ws,org_model_ws,
                                    grid_props=grid_props,hds_kperk=[0,0],remove_existing=True)
    pe = helper.draw(100)
    # zones using ibound values - vka in layer 2
    zone_props = ["upw.vka",1]
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,new_model_ws,org_model_ws,
                                   zone_props=zone_props,hds_kperk=[0,0],remove_existing=True)
    pe = helper.draw(100)
    # kper-level multipliers for boundary conditions
    bc_props = []
    for iper in range(m.nper):
        bc_props.append(["wel.flux",iper])
        #bc_props.append(["drn.elev",iper])
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,new_model_ws,org_model_ws,
                                    bc_props=bc_props,hds_kperk=[0,0],remove_existing=True)

    pe = helper.draw(100)
    zn_arr = np.loadtxt(os.path.join("..","examples","Freyberg_Truth","hk.zones"),dtype=int)
    k_zone_dict = {k:zn_arr for k in range(3)}


    obssim_smp_pairs = None
    helper = pyemu.helpers.PstFromFlopyModel(nam_file,new_model_ws,org_model_ws,
                                    pp_props=pp_props,
                                    const_props=const_props,
                                    grid_props=grid_props,
                                    zone_props=zone_props,
                                    temporal_bc_props=bc_props,
                                    spatial_bc_props=bc_props,
                                    remove_existing=True,
                                    obssim_smp_pairs=obssim_smp_pairs,
                                    pp_space=4,
                                    use_pp_zones=False,
                                    k_zone_dict=k_zone_dict,
                                    hds_kperk=[0,0],build_prior=False)
    pe = helper.draw(100)
    pst = helper.pst
    obs = pst.observation_data
    obs.loc[:,"weight"] = 0.0
    obs.loc[obs.obsnme.apply(lambda x: x.startswith("cr")),"weight"] = 1.0
    obs.loc[obs.weight>0.0,"obsval"] += np.random.normal(0.0,2.0,pst.nnz_obs)
    pst.control_data.noptmax = 0
    pst.write(os.path.join(new_model_ws,"freyberg_pest.pst"))
    cov = helper.build_prior(fmt="none",sparse=True)
    cov.to_coo(os.path.join("temp","cov.coo"))



def from_flopy_test():
    bd = os.getcwd()
    try:
        from_flopy()
    except Exception as e:
        os.chdir(bd)
        raise Exception("error in from_flopy:"+str(e))
    #print(os.getcwd())

def from_flopy_test_reachinput_test():
    bd = os.getcwd()
    try:
        from_flopy_reachinput()
    except Exception as e:
        os.chdir(bd)
        raise Exception("error in from_flopy_reachinput:"+str(e))
    #print(os.getcwd())


def from_flopy_reachinput():
    import pandas as pd
    """ test for building sfr pars from reachinput sfr and seg pars across all kper"""
    try:
        import flopy
    except:
        return
    import pyemu
    bd = os.getcwd()
    org_model_ws = os.path.join("..","examples","freyberg_sfr_reaches")
    nam_file = "freyberg.nam"
    new_model_ws = "temp_pst_from_flopy_reaches"

    m = flopy.modflow.Modflow.load(nam_file, model_ws=org_model_ws, check=False)

    helper = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws, org_model_ws,
                                             hds_kperk=[0, 0], remove_existing=True,
                                             model_exe_name="mfnwt", sfr_pars=True, sfr_obs=True)
    os.chdir(new_model_ws)
    with open("sfr_seg_pars.config",'r') as f:
        pars = {}
        for line in f:
            line = line.strip().split()
            pars[line[0]] = line[1]
    #tpl_df = pd.read_csv("{}.tpl".format(pars["mult_file"]), delim_whitespace=True,skiprows=1,index_col=0)
    #with open("{}.tpl".format(pars["mult_file"]),'r') as f:
    #    f.readline()
    #    tpl_df = pd.read_csv(f,index_col=0)
    #tpl_df = pd.read_csv("{}.tpl".format(pars["mult_file"]), index_col=0,skiprows=1)
    #mult_df = tpl_df.replace(r"^\~.*\~$",'100000.0', regex=True).copy()
    #mult_df.to_csv(pars["mult_file"], sep=',',index_label="iseg")
    
    pyemu.gw_utils.apply_sfr_parameters(reach_pars=True)
    os.chdir(bd)

def run_array_pars():
    import os
    import pyemu
    new_model_ws = "temp_pst_from_flopy"
    os.chdir(new_model_ws)
    pyemu.helpers.apply_array_pars()
    os.chdir('..')

def add_pi_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    pst.prior_information = pst.null_prior
    par_names = pst.parameter_data.parnme[:10]
    pst.add_pi_equation(par_names,coef_dict={par_names[1]:-1.0})
    pst.write(os.path.join("temp","test.pst"))

    pst = pyemu.Pst(os.path.join("temp","test.pst"))
    print(pst.prior_information)

def setattr_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    pst.model_command = 'test'
    assert isinstance(pst.model_command,list)
    pst.model_command = ["test","test1"]
    assert isinstance(pst.model_command,list)
    pst.write(os.path.join("temp","test.pst"))
    pst = pyemu.Pst(os.path.join("temp","test.pst"))
    assert isinstance(pst.model_command,list)


def add_pars_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    npar = pst.npar
    tpl_file = os.path.join("temp","crap.in.tpl")
    with open(tpl_file,'w') as f:
        f.write("ptf ~\n")
        f.write("  ~junk1   ~\n")
        f.write("  ~ {0}  ~\n".format(pst.parameter_data.parnme[0]))
    pst.add_parameters(tpl_file,"crap.in",pst_path="temp")
    assert npar + 1 == pst.npar
    assert "junk1" in pst.parameter_data.parnme
    assert os.path.join("temp","crap.in") in pst.input_files
    assert os.path.join("temp","crap.in.tpl") in pst.template_files

def add_obs_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    nobs = pst.nobs
    ins_file = os.path.join("temp", "crap.out.ins")
    out_file = os.path.join("temp","crap.out")
    oval = 1234.56
    with open(ins_file, 'w') as f:
        f.write("pif ~\n")
        #f.write("  ~junk1   ~\n")
        #f.write("  ~ {0}  ~\n".format(pst.parameter_data.parnme[0]))
        f.write("l1 w  !{0}!\n".format("crap1"))
    with open(out_file,"w") as f:
        f.write("junk1  {0:8.2f} \n".format(oval))
    pst.add_observations(ins_file,out_file, pst_path="temp")
    assert nobs + 1 == pst.nobs
    assert "crap1" in pst.observation_data.obsnme
    assert os.path.join("temp", "crap.out") in pst.output_files,str(pst.output_files)
    assert os.path.join("temp", "crap.out.ins") in pst.instruction_files
    print(pst.observation_data.loc["crap1","obsval"], oval)

def test_write_input_files():
    import os
    import shutil
    import numpy as np
    import pyemu
    from pyemu import Pst, pst_utils
    # creation functionality
    dir = os.path.join("..", "verification", "10par_xsec", "template_mac")
    if os.path.exists("temp_dir"):
        shutil.rmtree("temp_dir")
    shutil.copytree(dir,"temp_dir")
    os.chdir("temp_dir")
    pst = Pst(os.path.join("pest.pst"))
    pst.write_input_files()
    arr1 = np.loadtxt(pst.input_files[0])
    print(pst.parameter_data.parval1)
    pst.parameter_data.loc[:,"parval1"] *= 10.0
    pst.write_input_files()
    arr2 = np.loadtxt(pst.input_files[0])
    assert (arr1 * 10).sum() == arr2.sum()
    os.chdir("..")


def res_stats_test():
    import os
    import pyemu

    import os
    import numpy as np
    from pyemu import Pst, pst_utils
    # residual functionality testing
    pst_dir = os.path.join("pst")

    p = pyemu.pst_utils.generic_pst(["p1"],["o1"])
    try:
        p.get_res_stats()
    except:
        pass
    else:
        raise Exception()

    p = Pst(os.path.join(pst_dir, "pest.pst"))
    phi_comp = p.phi_components
    #print(phi_comp)
    df = p.get_res_stats()
    assert np.abs(df.loc["rss","all"] - p.phi) < 1.0e-6,"{0},{1}".format(df.loc["rss","all"],p.phi)
    for pc in phi_comp.keys():
        assert phi_comp[pc] == p.phi_components[pc]


def write_tables_test():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","freyberg_gr.pst"))
    group_names = {"w0":"wells t"}
    pst.write_par_summary_table(group_names=group_names,caption="par table")
    pst.write_obs_summary_table(group_names={"calhead":"calibration heads"},caption="obs table")


def flex_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst","pest_comments.pst"),flex=True)
    pst.with_comments = True
    pst.write(os.path.join("temp","pest_comments.pst"))


def test_e_clean():
    import os
    import pyemu

    pst_name = os.path.join("pst","test_missing_e.pst")
    try:
        pst = pyemu.Pst(pst_name)
    except:
        pass
    else:
        raise Exception()

    clean_name = os.path.join("temp","clean.pst")
    pyemu.pst_utils.clean_missing_exponent(pst_name,clean_name)
    pst = pyemu.Pst(clean_name)


def run_test():
    import os
    import pyemu

    pst = pyemu.Pst(os.path.join("pst","pest.pst"))
    #pst.run("pestchek")
    pst.write(os.path.join("temp","test.pst"))
    pst.run("pestchek")

def rectify_pgroup_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    npar = pst.npar
    tpl_file = os.path.join("temp", "crap.in.tpl")
    with open(tpl_file, 'w') as f:
        f.write("ptf ~\n")
        f.write("  ~junk1   ~\n")
        f.write("  ~ {0}  ~\n".format(pst.parameter_data.parnme[0]))
    #print(pst.parameter_groups)

    pst.add_parameters(tpl_file, "crap.in", pst_path="temp")

    #print(pst.parameter_groups)
    pst.rectify_pgroups()
    #print(pst.parameter_groups)

    pst.parameter_groups.loc["pargp","inctyp"] = "absolute"
    print(pst.parameter_groups)
    pst.write(os.path.join('temp',"test.pst"))
    print(pst.parameter_groups)


def try_process_ins_test():
    import os
    import pandas as pd
    import pyemu

    ins_file = os.path.join("utils","BH.mt3d.processed.ins")
    df = pyemu.pst_utils.try_process_ins_file(ins_file)

    #df1 = pyemu.pst_utils._try_run_inschek(ins_file,ins_file.replace(".ins",""))
    df1 = pd.read_csv(ins_file.replace(".ins",".obf"), delim_whitespace=True, names=["obsnme","obsval"],index_col=0)
    #df1.index = df1.obsnme
    df1.loc[:,"obsnme"] = df1.index
    df1.index = df1.obsnme
    #df1 = df1.loc[df.obsnme,:]
    diff = df.obsval - df1.obsval
    print(diff.max(),diff.min())
    print(diff.sum())
    assert diff.sum() < 1.0e+10

def rectify_pgroup_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    npar = pst.npar
    tpl_file = os.path.join("temp", "crap.in.tpl")
    with open(tpl_file, 'w') as f:
        f.write("ptf ~\n")
        f.write("  ~junk1   ~\n")
        f.write("  ~ {0}  ~\n".format(pst.parameter_data.parnme[0]))
    #print(pst.parameter_groups)

    pst.add_parameters(tpl_file, "crap.in", pst_path="temp")

    #print(pst.parameter_groups)
    pst.rectify_pgroups()
    #print(pst.parameter_groups)

    pst.parameter_groups.loc["pargp","inctyp"] = "absolute"
    print(pst.parameter_groups)
    pst.write(os.path.join('temp',"test.pst"))
    print(pst.parameter_groups)

def sanity_check_test():
    import os
    import pyemu
    pst = pyemu.Pst(os.path.join("pst", "pest.pst"))
    pst.parameter_data.loc[:,"parnme"] = "crap"
    pst.observation_data.loc[:,"obsnme"] = "crap"

    pst.write(os.path.join("temp","test.pst"))

def pst_from_flopy_geo_draw_test():

    import shutil
    import numpy as np
    import pandas as pd
    try:
        import flopy
    except:
        return
    import pyemu
    org_model_ws = os.path.join("..","examples","freyberg_sfr_update")
    nam_file = "freyberg.nam"
    m = flopy.modflow.Modflow.load(nam_file, model_ws=org_model_ws, check=False)
    flopy.modflow.ModflowRiv(m,stress_period_data={0:[[0,0,0,30.0,1.0,25.0],
                                                      [0,0,1,31.0,1.0,25.0],
                                                      [0,0,1,31.0,1.0,25.0]]})
    org_model_ws = "temp"
    m.change_model_ws(org_model_ws)
    m.write_input()

    new_model_ws = "temp_pst_from_flopy"

    hds_kperk = []
    for k in range(m.nlay):
        for kper in range(m.nper):
            hds_kperk.append([kper, k])
    temp_bc_props = [["wel.flux",None]]
    spat_bc_props = [["riv.cond", 0], ["riv.stage", 0]]
    ph = pyemu.helpers.PstFromFlopyModel(nam_file, new_model_ws=new_model_ws,
                                         org_model_ws=org_model_ws,
                                         zone_props=[["rch.rech", 0], ["rch.rech", [1, 2]]],
                                         remove_existing=True,
                                         model_exe_name="mfnwt",temporal_bc_props=temp_bc_props,
                                         spatial_bc_props=spat_bc_props)

    num_reals = 100000
    pe1 = ph.draw(num_reals=num_reals,sigma_range=6)
    pyemu.Ensemble.reseed()
    pe2 = pyemu.ParameterEnsemble.from_gaussian_draw(ph.pst,ph.build_prior(sigma_range=6),num_reals=num_reals)

    mn1,mn2 = pe1.mean(),pe2.mean()
    sd1,sd2 = pe1.std(),pe2.std()

    diff_mn = mn1 - mn2
    diff_sd = sd1 - sd2
    #print(mn1,mn2)
    print(diff_mn)
    assert diff_mn.apply(np.abs).max() < 0.1
    print(diff_sd)
    assert diff_sd.apply(np.abs).max() < 0.1


if __name__ == "__main__":
    # pst_from_flopy_geo_draw_test()
    #try_process_ins_test()
    # write_tables_test()
    # res_stats_test()
    # test_write_input_files()
    # add_obs_test()
    # add_pars_test()
    # setattr_test()
    # run_array_pars()
    #flopy_test()
    # add_obs_test()
    #from_flopy_kl_test()
    from_flopy_reachinput()
    #plot_flopy_par_ensemble_test()
    # add_pi_test()
    # regdata_test()
    # nnz_groups_test()
    # regul_rectify_test()
    # derivative_increment_tests()
    # tied_test()
    # smp_test()
    # smp_dateparser_test()
    # pst_manip_test()
    # tpl_ins_test()
    # flex_test()
    # comments_test()
    # test_e_clean()
    # load_test()
    # flex_load_test()
    # res_test()
    # smp_test()
    # from_io_with_inschek_test()
    # pestpp_args_test()
    # reweight_test()
    # reweight_res_test()
    # run_test()
    # rectify_pgroup_test()
    # sanity_check_test()
