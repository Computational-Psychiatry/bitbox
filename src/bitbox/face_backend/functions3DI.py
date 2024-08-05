import numpy as np
import cvxpy as cp
from sklearn.impute import KNNImputer
import os
from sklearn.exceptions import ConvergenceWarning

from ..utilities import landmark_to_feature_mapper

def save_shape_and_texture(alpha, beta, sdir, shp_path, tex_path):
        IX  = np.loadtxt('%s/IX.dat' % sdir)
        IY  = np.loadtxt('%s/IY.dat' % sdir)
        IZ  = np.loadtxt('%s/IZ.dat' % sdir)
        
        TEX  = np.loadtxt('%s/TEX.dat' % sdir)
        
        tex_mu = np.loadtxt('%s/tex_mu.dat' % sdir)
        
        x0 = np.loadtxt('%s/X0_mean.dat' % sdir)
        y0 = np.loadtxt('%s/Y0_mean.dat' % sdir)
        z0 = np.loadtxt('%s/Z0_mean.dat' % sdir)
        
        x = (x0+(IX @ alpha)).reshape(-1,1)
        y = (y0+(IY @ alpha)).reshape(-1,1)
        z = (z0+(IZ @ alpha)).reshape(-1,1)
        
        tex = (tex_mu+(TEX @ beta)).reshape(-1, 1)
        np.savetxt(shp_path, np.concatenate((x,y,z), axis=1))
        np.savetxt(tex_path, tex)


def create_expression_sequence(epsilons, E):
    ps = []
    for t in range(epsilons.shape[0]):
        epsilon = epsilons[t,:]
        p = ((E @ epsilon)).reshape(-1,1)
        ps.append(p)
    return np.array(ps)[:,:,0]


def total_variance_rec(model_path, e0path, epath, morphable_model='BFMmm-19830'):        
    e1 = np.loadtxt(e0path)

    imputer = KNNImputer(n_neighbors=2, weights="uniform")

    for i in range(e1.shape[1]):
        e1[:,i:i+1] = imputer.fit_transform(e1[:,i:i+1])
    
    sdir = os.path.join(model_path, f'models/MMs/{morphable_model}/')
    li = np.loadtxt(f'{sdir}/li.dat').astype(int)

    T = e1.shape[0]
    K = e1.shape[1]

    sdir = os.path.join(model_path, 'models/MMs/%s' % morphable_model)
    EX  = np.loadtxt('%s/E/EX_79.dat' % sdir)[li,:]
    EY  = np.loadtxt('%s/E/EY_79.dat' % sdir)[li,:]
    EZ  = np.loadtxt('%s/E/EZ_79.dat' % sdir)[li,:]
    E = np.concatenate((EX, EY, EZ), axis=0)
    
    p = create_expression_sequence(e1, E)
    W = 120
    num_wins = int(T/W)+1
    Es = E

    es = []
    xprev = None
    lastpart = False
    for ti in range(num_wins):
        t0 = ti*W
        tf = (ti+1)*W+1
        
        if t0 >= T:
            break
        
        if tf >= T:
            tf = T
            W = tf-t0
            lastpart = True
                
        pc = p[t0:tf,:].T    
        x = cp.Variable((K,W+1-int(lastpart)))
        
        objective = cp.Minimize(cp.sum(cp.norm(x[:,:W-int(lastpart)]-x[:,1:W+1-int(lastpart)],2,axis=1)))
        constraints = [cp.norm(pc-(Es@x[:,:W+1-int(lastpart)]),2,axis=0) <= 2.75*np.ones((W+1-int(lastpart),))]
        
        if ti > 0:
            constraints.append(x[:,0] == xprev[:,-1])
        
        prob = cp.Problem(objective, constraints)
        x.value = e1[t0:tf,:].T      
        
        result = prob.solve(solver=cp.CLARABEL)
        xprev = x.value
        
        if lastpart:
            es.append(x.value.T)
        else:
            es.append(x.value[:,:W].T)

    ecomb = np.concatenate(es,)

    np.savetxt(epath, ecomb)
    
    
def total_variance_rec_pose(ppath, pnewpath):
    trans1 = np.loadtxt(ppath)[:,0:3]
    p1 = np.loadtxt(ppath)[:,3:6]
    a1 = np.loadtxt(ppath)[:,6:]

    imputer = KNNImputer(n_neighbors=2, weights="uniform")

    for i in range(p1.shape[1]):
        p1[:,i:i+1] = imputer.fit_transform(p1[:,i:i+1])
        
    for i in range(trans1.shape[1]):
        trans1[:,i:i+1] = imputer.fit_transform(trans1[:,i:i+1])

    T = p1.shape[0]
    K = p1.shape[1]

    W = 120
    num_wins = int(T/W)+1

    ps = []
    ts = []
    pprev = None
    tprev = None
    lastpart = False
    for ti in range(num_wins):
        t0 = ti*W
        tf = (ti+1)*W+1
        
        if t0 >= T:
            break
        
        if tf >= T:
            tf = T
            W = tf-t0
            lastpart = True 
        
        pc = p1[t0:tf,:].T    
        x = cp.Variable((K,W+1-int(lastpart)))
        
        objective = cp.Minimize(cp.sum(cp.norm(x[:,:W-int(lastpart)]-x[:,1:W+1-int(lastpart)],1,axis=1)))
        constraints = [cp.norm((pc-x[:,:W+1-int(lastpart)]),2,axis=0) <= 0.006*np.ones((W+1-int(lastpart),))]

        if ti > 0:
            constraints.append(x[:,0] == pprev[:,-1])
        
        prob = cp.Problem(objective, constraints)
        x.value = p1[t0:tf,:].T
        
        result = prob.solve(solver=cp.CLARABEL)
        pprev = x.value
        if lastpart:
            ps.append(x.value.T)
        else:
            ps.append(x.value[:,:W].T)
        
        tc = trans1[t0:tf,:].T    
        x = cp.Variable((K,W+1-int(lastpart)))
        
        objective = cp.Minimize(cp.sum(cp.norm(x[:,:W-int(lastpart)]-x[:,1:W+1-int(lastpart)],2,axis=1)))
        constraints = [cp.norm((tc-x[:,:W+1-int(lastpart)]),2,axis=0) <= 3.5*np.ones((W+1-int(lastpart),))]
        
        if ti > 0:
            constraints.append(x[:,0] == tprev[:,-1])
        
        prob = cp.Problem(objective, constraints)
        x.value = trans1[t0:tf,:].T
        
        result = prob.solve(solver=cp.CLARABEL)
        tprev = x.value
        
        if lastpart:
            ts.append(x.value.T)
        else:
            ts.append(x.value[:,:W].T)

    pcomb = np.concatenate(ps,)
    tcomb = np.concatenate(ts,)

    posenew = np.concatenate((tcomb, pcomb, a1), axis=1)
    np.savetxt(pnewpath, posenew)
    

def compute_canonicalized_landmarks(model_path, epath, lpath, morphable_model='BFMmm-19830'):
    sdir = os.path.join(model_path, 'models/MMs/%s' % morphable_model)
    
    sdir = os.path.join(model_path, f'models/MMs/{morphable_model}/')
    li = np.loadtxt(f'{sdir}/li.dat').astype(int)

    X0 = np.loadtxt(f'{sdir}/X0_mean.dat').reshape(-1,1)[li]
    Y0 = np.loadtxt(f'{sdir}/Y0_mean.dat').reshape(-1,1)[li]
    Z0 = np.loadtxt(f'{sdir}/Z0_mean.dat').reshape(-1,1)[li]
    shp0 = np.concatenate((X0, Y0, Z0), axis=0)

    EX  = np.loadtxt('%s/E/EX_79.dat' % sdir)[li,:]
    EY  = np.loadtxt('%s/E/EY_79.dat' % sdir)[li,:]
    EZ  = np.loadtxt('%s/E/EZ_79.dat' % sdir)[li,:]
    E = np.concatenate((EX, EY, EZ), axis=0)

    e = np.loadtxt(epath)
    p = create_expression_sequence(e, E)
    EX  = np.loadtxt('%s/E/EX_79.dat' % sdir)[li,:]
    EY  = np.loadtxt('%s/E/EY_79.dat' % sdir)[li,:]
    EZ  = np.loadtxt('%s/E/EZ_79.dat' % sdir)[li,:]

    T = e.shape[0]

    L = []

    for t in range(T):
        et = e[t,:].reshape(-1,1)
        dshp = E @ et
        shp = shp0+dshp
        x0 = shp[:51,0]
        y0 = -shp[51:2*51,0]
        z0 = shp[2*51:3*51,0]
        l = np.concatenate((x0.reshape(-1,1), y0.reshape(-1,1), z0.reshape(-1,1)), axis=1)
        l = l.reshape(-1,1).T
        L.append(l)

    np.savetxt(lpath, np.concatenate(L, axis=0), fmt='%.4f')
    
    
def compute_localized_expressions(model_path, smooth_expression_file, local_exp_coeffs_file, morphable_model='BFMmm-19830', normalize=True):   
    basis_version = '0.0.1.F591-cd-K32d'
    
    sdir = os.path.join(model_path, f'models/MMs/{morphable_model}/')
    localized_basis_file = os.path.join(model_path, f'models/MMs/{morphable_model}/E/localized_basis/v.{basis_version}.npy')
    basis_set = np.load(localized_basis_file, allow_pickle=True).item()
    
    # @TODO the code does not work for differential expression computation
    # but only for absolute expressions. It needs to be adapted to the case where
    # basis_set['use_abs'] is set to False!
    assert basis_set['use_abs']
    
    rel_ids = landmark_to_feature_mapper(scheme='ibug51')

    li = np.loadtxt(f'{sdir}/li.dat').astype(int)
    
    facial_feats = list(rel_ids.keys())

    epsilons = np.loadtxt(smooth_expression_file)

    T = epsilons.shape[0]

    Es = {}

    for feat in rel_ids:
        rel_id = rel_ids[feat]
        EX  = np.loadtxt('%s/E/EX_79.dat' % sdir)[li[rel_id],:]
        EY  = np.loadtxt('%s/E/EY_79.dat' % sdir)[li[rel_id],:]
        EZ  = np.loadtxt('%s/E/EZ_79.dat' % sdir)[li[rel_id],:]
        Es[feat] = np.concatenate((EX, EY, EZ), axis=0)
        
    ConvergenceWarning('ignore')

    C = []
    for feat in facial_feats:
        rel_id = rel_ids[feat]
        dp = create_expression_sequence(epsilons, Es[feat])
        dictionary = basis_set[feat]
        coeffs = dictionary.transform(dp).T
        
        # normalize
        # 'min_0.5pctl', 'max_99.5pctl', 'min_2.5pctl', 'max_97.5pctl', 'Q1', 'Q3', 'median', 'mean', 'std'
        if normalize:
            if hasattr(dictionary, 'stats'):
                stats = dictionary.stats
                # stats_Q1 = stats['Q1'].reshape([-1,1])
                # stats_Q3 = stats['Q3'].reshape([-1,1])
                stats_mean = stats['mean'].reshape([-1,1])
                stats_std = stats['std'].reshape([-1,1])
                
                # # remove outliers using interquartile range
                # IQR = stats_Q3 - stats_Q1
                # lower_bound = stats_Q1 - 1.5 * IQR
                # upper_bound = stats_Q3 + 1.5 * IQR
                # idx = (coeffs < lower_bound) | (coeffs > upper_bound)
                # coeffs[idx] = 0
                
                # normalize (0-mean, 1-std)
                coeffs = (coeffs - stats_mean) / stats_std
            else:
                print("Skipping normalization because stats on localized expressions is not available.")
                            

        C.append(coeffs)
        
    C = np.concatenate(C).T

    np.savetxt(local_exp_coeffs_file, C)