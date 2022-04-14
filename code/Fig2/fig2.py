# coding=utf-8
from lytools import *  ## pip install lytools==0.0.47
from scipy.stats import f_oneway
data_path = '../../data/Fig2'
land_path = '../../data/common_data/land_mask.tif'


def plot_spatial(fpath,vmin=None,vmax=None):
    ## plot spatial figure
    array = ToRaster().raster2array(fpath)[0]
    # mask nan values
    array[array < -9999] = np.nan
    # above 30 degree
    array = array[:120]
    # plot the spatial figure
    plt.figure(figsize=(8, 4))
    plt.imshow(array, cmap='Spectral_r', vmin=vmin, vmax=vmax, aspect='auto')
    plt.colorbar()
    # plot the land mask
    DIC_and_TIF().plot_back_ground_arr_north_sphere(land_path, aspect='auto')
    # set xticks and yticks
    plt.xticks([])
    plt.yticks([])
    plt.title('Average of SR and MR recovery time (months)')
    plt.show()
    pass

def plot_fig2a():
    '''
    Plot drought recovery spatial figure
    average of MR and SR recovery time (months)
    :return:
    '''
    # load data
    fpath = join(data_path, 'average_of_SR_MR_recovery.tif')
    # plot the spatial figure
    plot_spatial(fpath,vmin=0,vmax=6)

    pass

def plot_fig2b():
    '''
    Plot drought recovery spatial figure
    SR recovery time (months)
    :return:
    '''
    # load data
    fpath = join(data_path, 'SR_recovery.tif')
    # plot the spatial figure
    plot_spatial(fpath,vmin=0,vmax=4)

    pass

def plot_fig2c():
    '''
    Plot drought recovery spatial figure
    MR recovery time (months)
    :return:
    '''
    # load data
    fpath = join(data_path, 'MR_recovery.tif')
    # plot the spatial figure
    plot_spatial(fpath, vmin=1, vmax=8)

    pass

def plot_fig2d_2e():
    dataframe_path = '../../data/Fig2/drought_recovery.df'
    df = Tools().load_df(dataframe_path)
    lc_list = Tools().get_df_unique_val_list(df, 'lc')
    lc_list = lc_list[::-1]
    print(lc_list)
    winter_mark = [0, 1]
    winter_mark_str_dict = {0: 'SR', 1: 'MR'}
    # winter_mark = [1]
    timing_list = ['early', 'mid', 'late', ]
    lim_list = [
        (1.3, 2.),
        (3, 7.)
    ]
    plt.figure(figsize=(12, 6))
    flag = 1
    for w in winter_mark:
        df_w = df[df['winter_mark'] == w]
        for t in timing_list:
            df_t = df_w[df_w['timing'] == t]
            if flag == 3:
                flag += 1
                continue
            plt.subplot(2, 3, flag)
            flag += 1
            sns.barplot(data=df_t, x='lc', y='recovery_time', ci=99.999999, order=lc_list)
            mean_list = []
            for lc in lc_list:
                df_lc = df_t[df_t['lc'] == lc]
                y_val = df_lc['recovery_time'].to_list()
                y_mean = np.nanmean(y_val)
                mean_list.append(y_mean)
            print(mean_list)
            std = np.std(mean_list)
            print('std', std)
            # sns.barplot(data=df_t,x='lc',y='recovery_time',ci='sd',order=Global_vars().lc_list())
            title = '{} {} Growing season'.format(winter_mark_str_dict[w], t)
            plt.title(title)
            plt.ylabel('Drought recovery(months)')
            plt.xlabel('Landcover')
            print(title)
            print('---')
            plt.ylim(lim_list[w])
            plt.tight_layout()

    plt.show()

def plot_fig2d_2e_ANOVA_test():
    ## F_oneway test
    dataframe_path = '../../data/Fig2/drought_recovery.df'
    df = Tools().load_df(dataframe_path)
    Tools().print_head_n(df, 5)
    lc_list = Tools().get_df_unique_val_list(df, 'lc')
    winter_mark_str_dict = {0: 'SR', 1: 'MR'}
    # Capitalize ABC
    print('\n')
    print('Capitalize ABC\n')
    for winter in [0,1]:
        for timing in ['early', 'mid', 'late']:
            tested_groups = []
            for lc in lc_list:
                df_winter = df[df['winter_mark'] == winter]
                df_timing = df_winter[df_winter['timing']==timing]
                df_lc = df_timing[df_timing['lc']==lc]
                Y = df_lc['recovery_time']
                Y = Y.dropna()
                Y = np.array(Y,dtype=int)
                tested_groups.append(Y)
            f12,p12 = f_oneway(tested_groups[0],tested_groups[1])
            f13,p13 = f_oneway(tested_groups[0],tested_groups[2])
            f23,p23 = f_oneway(tested_groups[1],tested_groups[2])
            print('{} {} Forest,Shrublands:{}'.format(winter_mark_str_dict[winter],timing,p12))
            print('{} {} Forest,Grasslands:{}'.format(winter_mark_str_dict[winter],timing,p13))
            print('{} {} Shrublands,Grasslands:{}'.format(winter_mark_str_dict[winter],timing,p23))
            print('#'*80)


    # lowercase abc
    print('\n')
    print('lowercase abc\n')
    for winter in [0,1]:
        for lc in lc_list:
            tested_groups = []
            for timing in ['early', 'mid', 'late']:
                df_winter = df[df['winter_mark'] == winter]
                df_timing = df_winter[df_winter['timing']==timing]
                df_lc = df_timing[df_timing['lc']==lc]
                Y = df_lc['recovery_time']
                Y = Y.dropna()
                Y = np.array(Y,dtype=int)
                tested_groups.append(Y)
            f12,p12 = f_oneway(tested_groups[0],tested_groups[1])
            f13,p13 = f_oneway(tested_groups[0],tested_groups[2])
            f23,p23 = f_oneway(tested_groups[1],tested_groups[2])
            print('{} {} early,mid:{}'.format(winter_mark_str_dict[winter],lc,p12))
            print('{} {} early,late:{}'.format(winter_mark_str_dict[winter],lc,p13))
            print('{} {} mid,late:{}'.format(winter_mark_str_dict[winter],lc,p23))
            print('#'*80)


    pass


def plot_fig2f():
    dataframe_path = '../../data/Fig2/drought_recovery.df'
    # dataframe_path = '/Volumes/Ugreen_4T_25/project05_redo/new_2021_results/arr/Dataframe/Dataframe.df'
    df = Tools().load_df(dataframe_path)
    df = df.dropna()
    lc_var = 'lc'
    timing_var = 'timing'
    winter_mark_var = 'winter_mark'
    df_cross = Tools().cross_select_dataframe(df, lc_var, timing_var)
    ratio_dict = {}
    for lc, timing in df_cross:
        df_i = df_cross[(lc, timing)]
        # print(df_i)
        df_with_winter = df_i[df_i[winter_mark_var] == 1]
        ratio = len(df_with_winter) / len(df_i)
        ratio_dict[(lc, timing)] = ratio
    lc_location_dict = {'Grasslands': 3, 'Shrublands': 2, 'deciduous': 1, 'evergreen': 0}
    timing_location_dict = {'early': 0, 'mid': 1, 'late': 2}
    lc_location_dict_reverse = {v: k for k, v in lc_location_dict.items()}
    timing_location_dict_reverse = {v: k for k, v in timing_location_dict.items()}
    array = np.ones((4, 3))
    for lc, timing in ratio_dict:
        lc_location = lc_location_dict[lc]
        timing_location = timing_location_dict[timing]
        array[lc_location, timing_location] = ratio_dict[(lc, timing)]
    # print(array)
    plt.imshow(array, cmap='Blues', interpolation='nearest',aspect='auto')
    plt.xticks(np.arange(3), [timing_location_dict_reverse[i] for i in range(3)])
    plt.yticks(np.arange(4), [lc_location_dict_reverse[i] for i in range(4)])
    plt.colorbar()
    plt.tight_layout()
    plt.show()
    # print(ratio_dict)
    pass


def main():
    # plot_fig2a()
    # plot_fig2b()
    # plot_fig2c()
    # plot_fig2d_2e()
    # plot_fig2d_2e_ANOVA_test()
    # plot_fig2e()
    plot_fig2f()
    pass

if __name__ == '__main__':
    main()