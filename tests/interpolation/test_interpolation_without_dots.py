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
        "test": {
            "val": 5
        }
    }})
    OmegaConf.resolve(cfg)
    print(cfg)
    assert cfg.ctx.b.c == cfg.ctx.test.val