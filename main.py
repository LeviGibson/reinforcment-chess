import network
import chess
import play

trainer = play.NnomTrainer(
    syzygyPath="/home/levigibson/Documents/syzygy/",
    modelPath='network'
    )

trainer.train(1000)
