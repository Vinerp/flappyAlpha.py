import cx_Freeze

arquivo = [cx_Freeze.Executable(
    script="flappyAlpha.py", icon="bluebird-midflap.ico"
)]


cx_Freeze.setup(
    name="FlappyBird",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["background-day.png", "base.png", "bluebird-downflap.png", "bluebird-midflap.png", "bluebird-upflap.png", "flappyAlpha.py", "message.png", "pipe-red.png", "README.md", "setup.py", "tela-inicial.png" ]}},
    executables=arquivo
)
