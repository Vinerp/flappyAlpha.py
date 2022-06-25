import cx_Freeze

arquivo = [cx_Freeze.Executable(
    script="flappyAlpha.py", icon="bluebird-midflap.ico"
)]


cx_Freeze.setup(
    name="FlappyBird",
    options={"build_exe": {"packages": ["pygame"],}},
    executables=arquivo
)
