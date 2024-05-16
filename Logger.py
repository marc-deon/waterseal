import inspect
import config

class Logger:
    toFile = True
    toDisplay = True
    logPath = "log.txt"
    file = False

    lines = []

    @staticmethod
    def Log(*args, end="\n", sep=" "):
        callerframerecord = inspect.stack()[1]  # 0 represents this line
                                                # 1 represents line at caller
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        s = f"{info.filename.split('/')[-1]}({info.lineno}) {info.function}: "

        if Logger.toFile:
            if not Logger.file:
                Logger.file = open(Logger.logPath, 'w')

            Logger.file.write(s)

            line = sep.join(str(arg) for arg in args) + end
            Logger.file.write(line)

        # TODO: Because of the way line wrapping works, this won't always work properly
        if Logger.toDisplay and config.logPanel:
            line = sep.join(str(arg) for arg in args) + end
            Logger.lines.append(line)
            Logger.DisplayLog()
        
    @staticmethod
    def ClearLog():
        Logger.lines = []

    @staticmethod
    def DisplayLog():
        config.logPanel.erase()
        h = config.logPanel.h
        back = min(h-3, len(Logger.lines))
        for l in Logger.lines[-back:]:
            config.logPanel.addstr(str(l))
        config.logPanel.Draw()

    @staticmethod
    def LogDebug(*args, end="\n", sep=" "):
        callerframerecord = inspect.stack()[1]  # 0 represents this line
                                                # 1 represents line at caller
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        s = f"{info.filename.split('/')[-1]}({info.lineno}) {info.function}: "

        if Logger.toFile:
            if not Logger.file:
                Logger.file = open(Logger.logPath, 'w')

            Logger.file.write(s)

            line = sep.join(str(arg) for arg in args) + end
            Logger.file.write(line)

    @staticmethod
    def LogWarning(*args, end="\n", sep=" "):
        raise NotImplementedError()
