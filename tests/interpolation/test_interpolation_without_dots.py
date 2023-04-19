from omegaconf import OmegaConf


def test_interpolation_without_dots():
    cfg = OmegaConf.create({"ctx": {
        "a": 1,
        "d": "test",
        "b": {
            "a": 10,
            # "d": "test",
            "c": "${${d}.val}"
        },
        "other_val": -1,
        "test": {
            "val": 5,
            "val_copy": "${val}",
            "other_val": "${other_val}"  # check that it doesn't get stuck in an infinite loop
        }
    }})
    OmegaConf.resolve(cfg)
    print(cfg)
    assert cfg.ctx.b.c == cfg.ctx.test.val


def test_same_name_interp():
    cfg = OmegaConf.create({
        "a": {
            "a": 1
        },
        "test": {
            "a": "${.a}",
            "b": "${.c}",
            "c": 100
        }
    })

    OmegaConf.resolve(cfg)
    print(cfg)


def test_interpolation_to_parent_node():
    cfg = OmegaConf.create(
        {'_target_': 'multisys.training.utils.train', '_convert_': 'object', '_selectkwargs_': True, '_config_': True, 'save_path': '${path.save_model}/${.name}', 'name': '${.model.name}', 'model': {'_base_': '${model}', 'input_size': {'_target_': 'multisys.training.utils.get_input_size', 'env': '${...env}'}, 'output_size': {'_target_': 'multisys.training.utils.get_output_size', 'env': '${...env}'}, 'dt': {'_target_': 'multisys.utils.get_attr', 'optional': True, 'obj': '${...env}', 'attr': 'dt'}}, 'env': '${train_env}', 'trainer': {'_base_': '${training}'}, 'callbacks': {'loss_monitor': {'_target_': 'multisys.training.callbacks.LossMonitor', 'save_path': '${...save_path}/loss', 'stop_loss': '${...trainer.stop_loss}'}, 'model_checkpoint': {'_target_': 'multisys.training.callbacks.ModelCheckpoint', 'save_path': '${path.save_model}/${...name}', 'save_step': 100}, 'model_output_monitor': {'_target_': 'multiagent.training.callbacks.ModelOutputMonitor', 'save_path': '${...save_path}/model_output_monitor'}, 'val_loss_monitor': {'_target_': 'multisys.training.callbacks.ValidationLossMonitor', 'dataset': {'_target_': 'neurogym.Dataset', 'env': '${eval_env}', 'batch_size': 10, 'seq_len': {'_target_': 'multisys.utils.get_attr', 'obj': '${eval_env}', 'attr': 'seq_len'}, 'cache_len': 10000.0}, 'save_path': '${...save_path}/loss'}, 'model_transfer_output_monitor': {'_target_': 'multiagent.training.callbacks.ModelOutputMonitor', 'save_path': '${...save_path}/model_transfer_monitor', 'dataset': {'_target_': 'neurogym.Dataset', 'env': '${eval_env}', 'batch_size': '${training.batch_size}', 'seq_len': {'_target_': 'multisys.utils.utils.get_attr', 'obj': '${env}', 'attr': 'seq_len'}}}, 'hebbnet_monitor': {'_target_': 'multiagent.training.callbacks.HebbNetworkMonitor', 'save_path': '${...save_path}/hebbnet_monitor'}}, '_sweep_': ['model', 'env'], 'load': True}
    )
    print(OmegaConf.to_yaml(cfg))


def test_omegaconf_python():
    cfg = OmegaConf.create({
        "values": ["a", "b", "c"],
        # "test": "{{python: _out_ = 10+5}}",
        # "v": "{{python: _out_ = [v for v in ${values} if v != 'b'] }}"
        "v": "{{python: [v for v in ${values} if v != 'b'] }}"
    })
    OmegaConf.resolve(cfg)
    for k, v in cfg.items():
        print(k, v)
    # print(OmegaConf.to_yaml(cfg))
    # print(parse_python(cfg["v"]))


def test_omegaconf_python_dict():
    cfg = OmegaConf.create({
        "n": 3,
        "objects": "{{python: \
            {f'o{i}': f'object{i}'  for i in range(${n})} \
        }}"
    })
    OmegaConf.resolve(cfg)
    print(cfg.objects)


def test_omegaconf_python_case2():
    cfg = OmegaConf.create({
        "model": {
            "size": 20,
            "beta": "'{{python: ${size}+2}}'"  # need to use re.search and not re.match
        }
    })
    OmegaConf.resolve(cfg)
    print(cfg.model.beta)