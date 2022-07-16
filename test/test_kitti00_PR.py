#!/usr/bin/env python3
# Developed by Junyi Ma, Xieyuanli Chen, and Jun Zhang
# This file is covered by the LICENSE file in the root of the project OverlapTransformer:
# https://github.com/haomo-ai/OverlapTransformer/
# Brief: calculate PR curve and F1max using the prediction files generated by test_kitti00_prepare.py


import os
import sys
p = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
if p not in sys.path:
    sys.path.append(p)
    
import copy
import matplotlib.pyplot as plt
import numpy as np
import yaml
from sklearn import metrics



def cal_pr_curve(prediction_file_name, ground_truth_file_name):
    precisions = []
    recalls = []


    des_dists = np.load(prediction_file_name)['arr_0']
    des_dists = np.asarray(des_dists, dtype='float32')
    des_dists = des_dists.reshape((len(des_dists), 3))
    print('Load descrptor distances predictions with pairs of ', len(des_dists))
    print(des_dists.shape)

    ground_truth = np.load(ground_truth_file_name, allow_pickle='True')['arr_0']

    """Changing the threshold will lead to different test results"""
    for thres in np.arange(0.0, 0.6, 0.0001):
        print("thresh: ", thres)
        tps = 0
        fps = 0
        tns = 0
        fns = 0
        """Update the start frame index"""
        for idx in range(150,len(ground_truth)-1):
            gt_idxes = ground_truth[int(idx)]
            reject_flag = False

            if des_dists[des_dists[:,0]==int(idx),2][0]>thres:
                reject_flag = True
            if reject_flag:
                if not gt_idxes.any():
                    tns += 1
                else:
                    fns += 1
            else:
                if des_dists[des_dists[:,0]==int(idx),1][0] in gt_idxes:
                    tps += 1
                else:
                    fps += 1

        if fps == 0:
            precision = 1
        else:
            precision = float(tps) / (float(tps) + float(fps))
        if fns == 0:
            recall = 1
        else:
            recall = float(tps) / (float(tps) + float(fns))

        precisions.append(precision)
        recalls.append(recall)

        print("precision ", precision)
        print("recall ", recall)

    print("Highest precision: %s" % max(precisions))
    print("Highest recall: %s" % max(recalls))

    return precisions, recalls

"""Ploting and saving AUC."""
def plotPRC(precisions, recalls, print_2file=True):
    # initial plot
    plt.clf()

    if print_2file:
        save_name = './test_results_kitti/PR.png'

    recalls, precisions = (list(t) for t in zip(*sorted(zip(recalls, precisions), reverse=True)))
    auc = metrics.auc(recalls, precisions) * 100

    plt.plot(recalls, precisions, linewidth=1.0)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1])
    plt.xlim([0.0, 1])
    plt.title('auc = ' + str(auc))

    if print_2file:
        plt.savefig(save_name)

    plt.show()

"""Calculating Max F1 score."""
def cal_F1_score():
    pr_values = np.load('./test_results_kitti/PR.npz')
    f1_scores_max = -1
    for i in range(pr_values['precisions'].shape[0]):
        precision = pr_values['precisions'][i]
        recall = pr_values['recalls'][i]
        f1_score = 2 * (precision * recall) / (precision + recall + 1e-10)
        if f1_score > f1_scores_max:
            f1_scores_max = copy.deepcopy(f1_score)
    print("f1_score on KITTI test seq: ", f1_scores_max)


def test_with_PR(ground_truth_file_name):

    plot_curve = True
    save_pr_results = True
    print_2file = True


    prediction_file_name = "./test_results_kitti/predicted_des_L2_dis.npz"

    if not os.path.exists("./test_results_kitti/PR.npz"):
        precisions, recalls = cal_pr_curve(prediction_file_name, ground_truth_file_name)

        pr_values = np.asarray([precisions, recalls])
        pr_values = pr_values[:, np.argsort(pr_values[0, :])]

        if (plot_curve):
            plotPRC(pr_values[0], pr_values[1], print_2file)

        if (save_pr_results):
            np.savez_compressed("./test_results_kitti/PR", precisions=pr_values[0], recalls=pr_values[1])

    cal_F1_score()



if __name__ == "__main__":
    # load config ================================================================
    config_filename = '../config/config.yml'
    config = yaml.safe_load(open(config_filename))
    ground_truth_file_name = config["test_config"]["gt_file"]
    # ============================================================================

    """ground truth file follows OverlapNet"""
    test_with_PR(ground_truth_file_name)

