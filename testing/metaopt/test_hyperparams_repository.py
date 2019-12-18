import json
import os

from neuraxle.hyperparams.space import HyperparameterSamples
from neuraxle.metaopt.auto_ml import HyperparamsJSONRepository

HYPERPARAMS = {'learning_rate': 0.01}
FIRST_SCORE_FOR_TRIAL = 1


def test_hyperparams_repository_should_create_new_trial(tmpdir):
    hyperparams_json_repository = HyperparamsJSONRepository(tmpdir)
    hyperparams = HyperparameterSamples(HYPERPARAMS)

    hyperparams_json_repository.create_new_trial(hyperparams)

    path_join = os.path.join(tmpdir, 'NEW_' + hyperparams_json_repository._get_trial_hash(
        hyperparams.to_flat_as_dict_primitive()) + '.json')
    with open(path_join) as f:
        trial_json = json.load(f)
    assert trial_json['hyperparams'] == hyperparams.to_flat_as_dict_primitive()
    assert trial_json['score'] is None


def test_hyperparams_repository_should_load_all_trials(tmpdir):
    hyperparams_json_repository = HyperparamsJSONRepository(tmpdir)
    for i in range(2):
        hyperparams = HyperparameterSamples({'learning_rate': 0.01 + i * 0.01})
        hyperparams_json_repository.save_score_for_success_trial(hyperparams, i)

    trials = hyperparams_json_repository.load_all_trials()

    assert len(trials) == 2
    assert trials[0].hyperparams == HyperparameterSamples(
        {'learning_rate': 0.01 + 0 * 0.01}).to_flat_as_dict_primitive()
    assert trials[1].hyperparams == HyperparameterSamples(
        {'learning_rate': 0.01 + 1 * 0.01}).to_flat_as_dict_primitive()


def test_hyperparams_repository_should_save_failed_trial(tmpdir):
    hyperparams_json_repository = HyperparamsJSONRepository(tmpdir)
    hyperparams = HyperparameterSamples(HYPERPARAMS)

    hyperparams_json_repository._save_failed_trial_json(hyperparams, Exception('trial failed'))

    path_join = os.path.join(tmpdir, 'FAILED_' + hyperparams_json_repository._get_trial_hash(
        hyperparams.to_flat_as_dict_primitive()) + '.json')
    with open(path_join) as f:
        trial_json = json.load(f)
    assert trial_json['hyperparams'] == hyperparams.to_flat_as_dict_primitive()
    assert trial_json['score'] is None


def test_hyperparams_repository_should_save_success_trial(tmpdir):
    hyperparams_json_repository = HyperparamsJSONRepository(tmpdir)
    hyperparams = HyperparameterSamples(HYPERPARAMS)

    hyperparams_json_repository._save_successful_trial_json(hyperparams, FIRST_SCORE_FOR_TRIAL)

    path_join = os.path.join(tmpdir, str(float(FIRST_SCORE_FOR_TRIAL)).replace('.', ',') + '_' + hyperparams_json_repository._get_trial_hash(
        hyperparams.to_flat_as_dict_primitive()) + '.json')
    with open(path_join) as f:
        trial_json = json.load(f)
    assert trial_json['hyperparams'] == hyperparams.to_flat_as_dict_primitive()
    assert trial_json['score'] == FIRST_SCORE_FOR_TRIAL
