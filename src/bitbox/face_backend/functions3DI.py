import numpy as np
import cvxpy as cp
from sklearn.impute import KNNImputer
from sklearn.decomposition import DictionaryLearning


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


    li = [17286,17577,17765,17885,18012,18542,18668,18788,18987,19236,7882,7896,7905,7911,6479,7323,
        7922,8523,9362,1586,3480,4770,5807,4266,3236,10176,11203,12364,14269,12636,11602,5243,5875,
        7096,7936,9016,10244,10644,9638,8796,7956,7116,6269,5629,6985,7945,8905,10386,8669,7949,7229]

    T = e1.shape[0]
    K = e1.shape[1]

    sdir = model_path + 'models/MMs/%s' % morphable_model 
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
    sdir = model_path + 'models/MMs/%s' % morphable_model
    
    li = [17286,17577,17765,17885,18012,18542,18668,18788,18987,19236,7882,7896,7905,7911,6479,7323,
        7922,8523,9362,1586,3480,4770,5807,4266,3236, 10176,11203,12364,14269,12636,11602,5243,5875,
        7096,7936,9016,10244,10644,9638,8796,7956,7116,6269,5629,6985,7945,8905,10386,8669,7949,7229]

    li = np.array(li)

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
    
    
def compute_localized_expressions(model_path, canonical_lmks_file, local_exp_coeffs_file, morphable_model='BFMmm-19830'):
    basis_version = '0.0.1.4'
    
    sdir = model_path + f'models/MMs/{morphable_model}/'
    localized_basis_file = f'models/MMs/{morphable_model}/E/localized_basis/v.{basis_version}.npy'
    basis_set = np.load(localized_basis_file, allow_pickle=True).item()

    P = np.loadtxt(canonical_lmks_file)

    P0 = np.loadtxt(f'{sdir}/p0L_mat.dat')
    X0 = P0[:,0]
    Y0 = P0[:,1]
    Z0 = P0[:,2]

    rel_ids   = {'lb': np.array(list(range(0, 5))),
                'rb': np.array(list(range(5, 10))),
                'no': np.array(list(range(10, 19))),
                'le': np.array(list(range(19, 25))),
                're': np.array(list(range(25, 31))),
                'ul': np.array(list(range(31, 37))+list(range(43, 47))),
                'll': np.array(list(range(37, 43))+list(range(47, 51)))}

    facial_feats = list(rel_ids.keys())

    T = P.shape[0]

    C = []
    for t in range(T):
        cur = []
        for feat in facial_feats:
            rel_id = rel_ids[feat]
        
            p = P[t,:]
            x = p[::3]
            y = p[1::3]
            z = p[2::3]
            
            dx = x-X0
            dy = y-Y0
            dz = z-Z0
            
            # @TODO the following code does not work for differential expression computation
            # but only for absolute expressions. It needs to be adapted to the case where
            # basis_set['use_abs'] is set to False!
            dp = np.concatenate((dx[rel_id], dy[rel_id], dz[rel_id]))
            dictionary = basis_set[feat]
            # dictionary.set_params(transform_max_iter=2000)
            coeffs = dictionary.transform(dp.reshape(1,-1)).T
            cur.append(coeffs)
        
        C.append(np.concatenate(cur).reshape(-1,))
    C = np.array(C)

    np.savetxt(local_exp_coeffs_file, C)