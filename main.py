import network
import chess
import play

trainer = play.NnomTrainer(
    syzygyPath="/home/levigibson/Documents/static/arenalinux_64bit_3.10beta/TB/syzygy/",
    modelPath='network'
    )

trainer.train(1000)
