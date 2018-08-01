def logger(logInput, logType, file = "log.txt"):
    return
    log = ''
    if logType == 'game':
        log = 'game: ' + str(logInput)
        log += '\n'
    elif logType == 'round':
        log += '\n'
        log = 'BB: ' + str(logInput['BB']) + ', SB: ' + str(logInput['SB']) + ', ante: ' + str(logInput['ante']) + ', games: ' + str(logInput['games'])
        log += '\n'
    elif logType == 'playerTurn':
        # tableData = logInput["tableData"]
        # log = logInput['name'] + '(' + str(logInput['stack']) + ') - ' + str(tableData["position"]) + '/' + str(tableData["firstBetPositionName"]) + ' ' + str(tableData["hand"][0]) + ' ' + str(tableData["hand"][1]) + ' ' + str(logInput['betAmount'])
        log = logInput['name'] + '(' + str(logInput['stack']) + '/' + str(logInput['betAmount']) + ' + ' + str(logInput['bet']) + ') | '
    elif  logType == 'potBefore':
        return
        log = 'pot before: '
        for index, playerPot in enumerate(logInput):
            log += str(index) + ' - ' + str(playerPot) + ', '
    elif logType == 'potAfter':
        return
        log = 'pot after: '
        for index, playerPot in enumerate(logInput):
            log += str(index) + ' - ' + str(playerPot) + ', '
    elif logType == 'places':
        return
        #log = 'places: '
        #for index, place in enumerate(logInput):
            #log += str(index) + ': ' + str(place) + ', '
    elif logType == 'hands':
        return
        #log = 'hands: '
        #for hand in logInput:
            #log += str(hand["index"]) + ' - ' + str(hand["score"]) + ', '
    elif logType == 'dqnPlace':
        log = 'Dqn finished ' + str(logInput)
    elif logType == 'tableNr':
        log = '\n'
        log += 'table: ' + str(logInput)
        log += '\n'
    elif logType == 'minMax':
        log = '\n'
        log += 'min/max/maxCnt: ' + str(logInput['min']) + '/' + str(logInput['max']) + '/' + str(logInput['maxCnt'])
        log += '\n'
    elif logType == 'default':
        log = logInput
    f = open(file, "a")
    f.write(log)