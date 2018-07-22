screen = Screen()
tableData = ''
maxGames = 5
tableScreenShot = None
gamesPlayed = 0
gameId = None
positions = ['B', 'SB', 'BB', 'UTG', 'UTG+1', 'UTG+2', 'MP1', 'MP2', 'C']
positionsMap = {'B': 6, 'SB': 7, 'BB': 8, 'UTG': 0, 'UTG+1': 1, 'UTG+2': 2, 'MP1': 3, 'MP2': 4, 'C': 5}
positionsCorrectionArr = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 4, 5, 6, 7, 8], [0, 1, 2, 5, 6, 7, 8], [0, 1, 2, 6, 7, 8], [0, 1, 2, 7, 8], [0, 1, 2, 8], [0, 1, 2], [1, 2]]
badCards = ["7h"]
table = Region(333,151,999,719)
import subprocess
import json
import random
import time
import uuid
class FileSystem():
    def __init__(self):
        self.pyscript = "/home/andrei/sikuli/projects/poker_1.7.sikuli/extractText.py"
        self.logsToDbScript = "/home/andrei/sikuli/projects/poker_1.7.sikuli/logsToDb.py"
        self.python = "/usr/bin/python"
        self.chart0 = "/home/andrei/sikuli/projects/poker_1.7.sikuli/chart0.json"
        self.chart1 = "/home/andrei/sikuli/projects/poker_1.7.sikuli/chart1.json"
    def readImage(self, imgPath, scaler):
        return subprocess.check_output([self.python, self.pyscript, imgPath, scaler]).strip(' \t\n\r')
    def readJson(self, path):
        with open(path) as data_file:    
            return json.load(data_file)
    def logsToDatabase(self, msg, action, screenshot, card1, card2, hand, firstbet, playercnt, money, pot, sb, bb, ante, playerPos, bbs, first, gameId):
         return subprocess.check_output([self.python, self.logsToDbScript, msg, action, screenshot, card1, card2, hand, firstbet, playercnt, money, pot, sb, bb, ante, playerPos, bbs, first, gameId])
class Player():
    def __init__(self):
        self.nameImgs = ["1509878194711.png", "1509882684344.png", "1509885982418.png",  "1509878194711.png"]
        self.turnImg =  "1509878194711.png"
        self.playerRegion = ''
                                                             
        self.deck = [{'val':'2', 'int': 2, 'suit': 'D', 'img':"1510034658432.png"}, {'val':'3', 'int': 3, 'suit': 'D', 'img':"1510034588633.png" }, {'val':'4', 'int': 4, 'suit': 'D', 'img':"1510034582844.png" }, {'val':'5', 'int': 5, 'suit': 'D', 'img':"1510035196254.png" },{'val':'6', 'int': 6, 'suit': 'D', 'img':"1510035078379.png"  },{'val':'7', 'int': 7, 'suit': 'D', 'img':"1510080984197.png"},{'val':'8', 'int': 8, 'suit': 'D', 'img':"1510034735732.png"},{'val':'9', 'int': 9, 'suit': 'D', 'img': "1510035054464.png"},{'val':'10', 'int': 10, 'suit': 'D', 'img':"1510081512228.png" },{'val':'J', 'int': 11, 'suit': 'D', 'img':"1510035111947.png"},{'val':'Q', 'int': 12, 'suit': 'D', 'img':"1510034952629.png"},{'val':'K', 'int': 13, 'suit': 'D', 'img':"1510034556099.png"},{'val':'A', 'int': 14, 'suit': 'D', 'img':"1510035100245.png"},
                {'val':'2', 'int': 2, 'suit': 'C', 'img':"1510034702893.png"}, {'val':'3', 'int': 3, 'suit': 'C', 'img': "1510034897822.png"},{'val':'4', 'int': 4, 'suit': 'C', 'img':"1510034565598.png"},{'val':'5', 'int': 5, 'suit': 'C', 'img':"1510081266167.png"},{'val':'6', 'int': 6, 'suit': 'C', 'img':"1510035276758.png"},{'val':'7', 'int': 7, 'suit': 'C', 'img':"1510035244228.png"},{'val':'8', 'int': 8, 'suit': 'C', 'img':"1510035146743.png"},{'val':'9', 'int': 9, 'suit': 'C', 'img':"1510034876746.png"},{'val':'10', 'int': 10, 'suit': 'C', 'img':"1510035286443.png"},{'val':'J', 'int': 11, 'suit': 'C', 'img':"1510035233290.png"},{'val':'Q', 'int': 12, 'suit': 'C', 'img':"1510035021792.png"},{'val':'K', 'int': 13, 'suit': 'C', 'img':"1510034686963.png"},{'val':'A', 'int': 14, 'suit': 'C', 'img':"1510035980728.png"},
                {'val':'2', 'int': 2, 'suit': 'S', 'img':"1510034991769.png"}, {'val':'3', 'int': 3, 'suit': 'S', 'img':"1510036544751.png"},{'val':'4', 'int': 4, 'suit': 'S', 'img':"1510034916337.png"},{'val':'5', 'int': 5, 'suit': 'S', 'img':"1510034695360.png"},{'val':'6', 'int': 6, 'suit': 'S', 'img':"1510035090144.png"},{'val':'7', 'int': 7, 'suit': 'S', 'img':"1510034845297.png"},{'val':'8', 'int': 8, 'suit': 'S', 'img':"1510034747249.png"},{'val':'9', 'int': 9, 'suit': 'S', 'img':"1510768869456.png"},{'val':'10', 'int': 10, 'suit': 'S', 'img':"1510034810477.png"},{'val':'J', 'int': 11, 'suit': 'S', 'img':"1510036166292.png"},{'val':'Q', 'int': 12, 'suit': 'S', 'img':"1510034933616.png"},{'val':'K', 'int': 13, 'suit': 'S', 'img':"1510035035424.png"},{'val':'A', 'int': 14, 'suit': 'S', 'img':"1510035123293.png"},
                {'val':'2', 'int': 2, 'suit': 'H', 'img':"1510036359805.png"}, {'val':'3', 'int': 3, 'suit': 'H', 'img':"1510034605652.png"},{'val':'4', 'int': 4, 'suit': 'H', 'img':"1510035312711.png"},{'val':'5', 'int': 5, 'suit': 'H', 'img':"1510034712660.png"},{'val':'6', 'int': 6, 'suit': 'H', 'img':"1510035257710.png"},{'val':'7', 'int': 7, 'suit': 'H', 'img':"1510768577710.png"},{'val':'8', 'int': 8, 'suit': 'H', 'img':"1510769382715.png"},{'val':'9', 'int': 9, 'suit': 'H', 'img':"1510081188740.png"},{'val':'10', 'int': 10, 'suit': 'H', 'img':"1510035130676.png"},{'val':'J', 'int': 11, 'suit': 'H', 'img':"1510081013362.png"},{'val':'Q', 'int': 12, 'suit': 'H', 'img':"1510034888864.png"},{'val':'K', 'int': 13, 'suit': 'H', 'img':"1510034968070.png"},{'val':'A', 'int': 14, 'suit': 'H', 'img':"1510034795549.png"},]
        self.hand = [None, None]
        self.player = None
        self.moneyImg = None
        self.money = None
        
    def getCards(self):
        self.hand = [None, None];
        global tableData
        for card in self.deck:
            pat = Pattern(card['img']).exact()
            if(self.playerRegion.exists(pat, 0)):
                if self.hand[0] == None:
                    self.hand[0] = card
                else:
                    self.hand[1] = card
        if self.hand[0] == None or self.hand[1] == None:
            tableData += 'error: player cards not found/'
            
    def getPlayer(self, region):
        global tableData
        self.playerRegion = region
        player = ''
        for img in self.nameImgs:
            try:
                player = region.find(img)
            except:
                self.player = None
            finally:
                self.player = player
        if self.player == None:
            tableData += 'error: player image not found/'
        
    def getCurrentMoney(self):
        global tableData
        self.moneyImg = self.player.offset(0, self.player.h)
        filePath = screen.capture(self.moneyImg).getFilename()
        moneyRaw = fileSystem.readImage(filePath, "2")
        try:
            self.money = int(moneyRaw.replace("'","").replace("[", "").replace("]", "").replace(".", "").replace(",", "").replace(".","").replace('$',""))
        except:
            tableData += "error: player money extraction error/"
            self.money = 1000000
            
    def cleardata(self):
        self.playerRegion = None
        self.hand = [None, None]
        self.player = None
        self.moneyImg = None
        self.money = None
        
class Turn():
    def __init__(self):
        global table
        self.player = Player()
        self.playerCnt = 0
        self.playerImg = "1509878323729.png"
        self.sittingOutImg = "1508448132852.png"
        self.dealerImg = "1509879042207.png"
        self.emptySeatImg = "1509878434027.png"
        self.foldButton ="1509878390892.png"
        self.checkButton = "1510336111993.png"
        self.sittingOutImg = "1510335655422.png"
        #self.registerImg = "1510335954698.png"
        self.registerImg = "1510778985352.png"
        self.confirmRegisterImg = "1510337044502.png"
        self.windowControlsImg = "1510682326829.png"
        self.windowControlsButton = None
        self.windowExpandImg = "1510334831977.png"
        self.maxButton = "1509878549382.png"
        self.table = table
        self.randomClickRegion = self.getRegion(self.table, 0.3, 0.3, 0.7, 0.3)
        self.potImg = "potImg.png"
        self.potNums = ["0_pot.png", "1_pot.png", "2_pot.png", "3_pot.png", "4_pot.png", "5_pot.png", "6_pot.png", "7_pot.png", "8_pot.png", "9_pot.png"]
        self.firstBet = None
        self.betPositions = []
        self.blImg = "blImg.png"
        
        self.betImg1 = "1509880527649.png"
        self.blNums = [{"img":"0_bl.png", "val":"0"}, {"img":"1_bl.png", "val":"1"}, {"img": "2_bl.png", "val":"2"}, {"img": "3_bl.png", "val":"3"}, {"img": "4_bl.png", "val":"4"}, {"img": "5_bl.png", "val":"5"}, {"img": "6_bl.png", "val":"6"}, {"img": "7_bl.png", "val":"7"}, {"img": "8_bl.png", "val":"8"}, {"img": "9_bl.png", "val":"9"}, {"img": "$_bl.png", "val":"$"}, {"img": "d_bl.png", "val":"/"}, {"img": "1509893676247.png", "val": "Ante"}]
        #test 
        #self.blNums = [{"img":"0_bl_test.png", "val":"0"}, {"img":"1_bl_test.png", "val":"1"}, {"img": "2_bl_test.png", "val":"2"}, {"img": "3_bl_test.png", "val":"3"}, {"img": "4_bl_test.png", "val":"4"}, {"img": "5_bl_test.png", "val":"5"}, {"img": "6_bl_test.png", "val":"6"}, {"img": "7_bl_test.png", "val":"7"}, {"img": "8_bl_test.png", "val":"8"}, {"img": "9_bl_test.png", "val":"9"}, {"img": "$_bl_test.png", "val":"$"}, {"img": "d_bl_test.png", "val":"/"}, {"img": "ante_bl_test.png", "val": "Ante"}]
        self.blRegion = None
        self.potAmmountRegion = None
        self.potNumsArr = []
        self.openPositions = [];
        self.tableClear = Region(self.table.x, self.table.y, self.table.w, self.table.h / 20 * 17)
        self.controlsRegion = Region(self.table.x + self.table.w / 10 * 5, self.table.y + self.table.h / 10 * 8, self.table.w / 10 * 5, self.table.h / 10 * 2)
        self.pushButtonRegion = Region(self.controlsRegion.x + self.controlsRegion.w / 10 * 7, self.controlsRegion.y + self.controlsRegion.h / 10 * 6, self.controlsRegion.w / 10 * 3, self.controlsRegion.h / 10 * 4)
        self.tableLength = 9
        #screen.capture(self.controlsRegion).getFilename()
        #screen.capture(self.pushButtonRegion).getFilename()
        self.nineTable = [{'id': 0, 'bet': 0, 'status': 'active', 'position': '', 'region': self.getRegion(self.tableClear, 0.58, 0.58, 0.3, 0.28)},
                {'id': 1, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.45, 0.58, 0.15, 0.3)},
                {'id': 2, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.15, 0.58, 0.3, 0.3)},
                {'id': 3, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0, 0.45, 0.32, 0.25)},
                {'id': 4, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.05, 0.15, 0.2, 0.32)},
                {'id': 5, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.3, 0.06, 0.2, 0.4)},
                {'id': 6, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.5, 0.06, 0.2, 0.4)},
                {'id': 7, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.65, 0.06, 0.25, 0.4)},
                {'id': 8, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.7, 0.45, 0.32, 0.25)}]
        #for player in self.nineTable:
            #screen.capture(player['region']).getFilename()
        self.sevenTable = [{'id': 0, 'bet': 0, 'status': 'active', 'position': '', 'region': self.getRegion(self.tableClear, 0.70, 0.55, 0.33, 0.35)},
                {'id': 1, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.40, 0.62, 0.25, 0.5)},
                {'id': 2, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.1, 0.55, 0.25, 0.4)},
                {'id': 3, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.01, 0.30, 0.3, 0.27)},
                {'id': 4, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.23, 0.06, 0.2, 0.35)},
                {'id': 5, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.60, 0.06, 0.2, 0.35)},
                {'id': 6, 'bet': 0, 'status': 'empty', 'position': '', 'region': self.getRegion(self.tableClear, 0.75, 0.30, 0.22, 0.32)}]
        #for player in self.sevenTable:
            #screen.capture(player['region']).getFilename()
        self.tableLayouts = [self.nineTable, self.sevenTable]
        self.players = []
        self.sittingOut = []
        self.emptySeat = []
        self.tableInfoRaw = ""
        self.tableInfo = {'SB': None, 'BB': None, 'ante': None, 'tournament':'', 'table':'', 'pot': None}
        self.turnData = {'msg': None, 'action': None, 'screenshot': None, 'card1': None, 'card2': None, 'hand': None, 'firstbet': None, 'playerCnt': None, 'money': None, 'pot': None, 'SB': None, 'BB': None, 'ante': None, 'playerPos': None, 'bbs': None, 'first': None}

    def getRegion(self, region, x, y, w, h):
        return Region(int(round(region.x * 1.0 + region.w * 1.0 * x, 0)), int(round(region.y * 1.0 + region.h * 1.0 * y, 0)), int(round(region.w * 1.0 * w, 0)), int(round(region.h * 1.0 * h, 0)))
        
    def cleardata(self):
        self.player.cleardata()
        self.playerCnt = 0
        self.firstBet = None
        self.betPositions = []
        self.blRegion = None
        self.potAmmountRegion = None
        self.potNumsArr = []
        self.openPositions = [];
        self.players = []
        self.sittingOut = []
        self.emptySeat = []
        self.tableInfoRaw = ""
        self.tableInfo = {'SB': None, 'BB': None, 'ante': None, 'tournament':'', 'table':'', 'pot': None}
        self.turnData = {'msg': None, 'action': None, 'screenshot': None, 'card1': None, 'card2': None, 'hand': None, 'firstbet': None, 'playerCnt': None, 'money': None, 'pot': None, 'SB': None, 'BB': None, 'ante': None, 'playerPos': None, 'bbs': None, 'first': None}
        
    def getTableLayout(self):
        global tableData
        for layout in self.tableLayouts:
            thisLayout = False
            for nameImg in self.player.nameImgs:
                pat = Pattern(nameImg).exact()
                #screen.capture(layout[0]['region']).getFilename()
                if layout[0]['region'].exists(pat, 0):
                    self.players = layout
                    thisLayout = True
                    self.tableLength = len(layout)
                    break
                if thisLayout == True:
                    break
        if len(self.players) == 0:
            tableData += 'error: player image not found/'
        #screen.capture(self.players[0]["region"]).getFilename()

    def takeTableScreenShot(self):
        global tableScreenShot
        tableScreenShot = screen.capture(self.table).getFilename()
        self.turnData['screenshot'] = tableScreenShot;

    def waitForTournamentStart(self):
        while not self.table.exists(self.windowControlsImg):
            sleep(1)
        self.takeTableScreenShot()
        self.windowControlsButton = self.table.find(self.windowControlsImg)
        print 'start new'
        return 'startNew'
        
    def waitForYourTurn(self):
        global tableData
        self.table.setAutoWaitTimeout(0);
        while not self.table.exists(self.player.turnImg):
            try:
                sittingOutBtn = self.table.find(self.sittingOutImg)
                self.clickButtonRandom(sittingOutBtn)
            except:
                try:
                    registerImg = self.table.find(self.registerImg)
                    self.clickButtonRandom(registerImg)
                    sleep(3)
                    confirmBtn = self.table.find(self.confirmRegisterImg)
                    self.clickButtonRandom(confirmBtn)
                    while not self.table.exists(self.windowControlsImg):
                        sleep(1)
                    self.takeTableScreenShot()
                    self.windowControlsButton = self.table.find(self.windowControlsImg)
                    
                    print 'start new'
                    return 'startNew'                   
                except:
                    pass
            sleep(1)
        self.takeTableScreenShot();
        self.getTableLayout()
        try:
            self.countPlayers()
        except:
            tableData += "player count error/"
            return "fold"
        try:
            positions = self.getPlayersPositions()
            self.turnData['playerPos'] = positions           
        except:
            tableData += "error: get player positions error/"
            return "fold"
        try:
            self.player.getPlayer(self.players[0]['region'])
        except:
            tableData += "error: get player error/"
            return "fold"
        try:
            self.player.getCurrentMoney()
            self.turnData['money'] = self.player.money
        except:
            tableData += "error: get player money error/"
            return "fold"
        try:
            self.player.getCards()
            if self.player.hand[0] == None:
                self.turnData['card1'] = None
            else:
                self.turnData['card1'] = self.player.hand[0]['val']+self.player.hand[0]['suit']
            if self.player.hand[1] == None:
                self.turnData['card2'] = None
            else:
                self.turnData['card2'] = self.player.hand[1]['val']+self.player.hand[1]['suit']
        except:
            tableData += "error: get player cards error/"
            return "fold"
        try:
            self.getBlinds()
        except:
            tableData += "error: get blinds error/"
            return "fold"
        try:
            advice = self.giveAdvice()
            return advice.split("/")[0]
        except:
            tableData += "error: give advise error/"
            return "fold"
        
    def getBlinds(self):
        global tableData
        tableInfoImg = Region(self.table.x + self.table.w / 10 * 2, self.table.y, self.table.w / 10 * 6, self.table.h / 100 * 13)
        try:
            blRegion = tableInfoImg.find(self.blImg);
        except:
            tableData += 'error: blinds image not found in table header/'
            self.tableInfo = False
        try:
            self.blRegion = Region(blRegion.x + blRegion.w, blRegion.y, blRegion.w * 5, blRegion.h)
        except:
            tableData += 'error: blinds not found in table header/'
            self.tableInfo = False
        self.tableInfoRaw = self.getBlNumbers()
        if len(self.tableInfoRaw) == 0:
            tableData += 'error: blind data not found in the table header/'
            self.tableInfo = False
        else:
            if(self.tableInfoRaw.find("Ante") != -1):
                blindSeparator = "Ante"
                self.tableInfo['ante'] = int(self.tableInfoRaw.split("Ante")[1].replace("$", ""))
            else:
                blindSeparator = " "
                self.tableInfo['ante'] = 0
            self.turnData['ante'] = self.tableInfo['ante']
            blinds = self.tableInfoRaw.split('/')
            self.tableInfo['SB'] = int(blinds[0].replace("$", ""))
            self.tableInfo['BB'] = int(blinds[1].split(blindSeparator)[0].replace("$", ""))
            self.turnData['SB'] = self.tableInfo['SB']
            self.turnData['BB'] = self.tableInfo['BB']
            try:
                potRegion = tableInfoImg.find(self.potImg)
            except:
                tableData += "error: potImg not found/"
            self.potAmmountRegion = Region(potRegion.x + potRegion.w, potRegion.y - potRegion.h / 3, potRegion.w * 3, potRegion.h * 2)
            self.tableInfo['pot'] = self.getPotNumbers()
            self.turnData['pot'] = self.tableInfo['pot']
            if self.tableInfo['pot'] == None:
                tableData += "error - potNumbers not found/"

    def giveAdvice(self):
        global tableData
        charts = [fileSystem.readJson(fileSystem.chart0), fileSystem.readJson(fileSystem.chart1)];
        chartNr = 0;
        anteCof = 0;
        first = self.checkFirstIn();
        BBCount = self.countBB()
        self.turnData['bbs'] = BBCount
        self.turnData['first'] = first
        if BBCount == 0:
            return 'push'
        
        if(BBCount > 15):
            tableData += 'too many BBs/'
            return 'fold/'
        hand = self.getSimpleHand()
        self.turnData['hand'] = str(hand[0])+str(hand[1])+str(hand[2])
        position = self.players[0]['position']
        if(first):
            chartNr = 0 
        else:
            chartNr = 1
        if(chartNr == 0):
            if(position == 'BB'):
                return 'push'
            actionData = charts[chartNr][position][str(BBCount)]
            hands = actionData[hand[2]]
            percent = ''
            if(actionData['%']):
                percent = str(actionData['%']) + ' %'
            else:
                percent = 'no chart available'
            
            if(hand[2] == 'p'):
                if(hands[1] == '+'):
                    if(hand[0] >= hands[0]):
                        return 'push/percent: '+percent
                return 'fold'
            else:
                for cards in actionData['o']['++']:
                    if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                        return 'push/percent: '+percent
                for cards in actionData['o']['+']:
                    if(hand[0] == cards[0] and hand[1] >= cards[1]):
                        return 'push/percent: '+percent
                for cards in actionData['o']['=']:
                    if(hand[0] == cards[0] and hand[1] == cards[1]):
                        return 'push/percent: '+percent
                if(hand[2] == 's'):
                    for cards in actionData['s']['++']:
                        if(hand[0] >= cards[0] and hand[1] >= cards[1]):
                            return 'push/percent: '+percent
                    for cards in actionData['s']['+']:
                        if(hand[0] == cards[0] and hand[1] >= cards[1]):
                            return 'push/percent: '+percent
                    for cards in actionData['s']['=']:
                        if(hand[0] == cards[0] and hand[1] == cards[1]):
                            return 'push/percent: '+percent
            return 'fold'
        elif chartNr == 1:
            firstBet = False
            if self.firstBet == 'UTG' or self.firstBet == 'UTG+1' or self.firstBet == 'UTG+2':
                firstBet = 'E'
            elif self.firstBet == 'MP1' or self.firstBet == 'MP2':
                firstBet = 'M'
            elif self.firstBet == 'C':
                firstBet = 'C'
            elif self.firstBet == 'B':
                firstBet = 'B'
            else:
                firstBet = 'SB'
            self.turnData['firstbet'] = firstBet
            actionData = charts[chartNr][position][firstBet]           
            if str(hand[0]) in actionData:
                if str(hand[1]) in actionData[str(hand[0])]:
                    if str(hand[2]) in actionData[str(hand[0])][str(hand[1])]:
                        maxBbs = actionData[str(hand[0])][str(hand[1])][str(hand[2])]
                        if BBCount <= maxBbs:
                            return 'push'
            return 'fold'
            
        
    def countBB(self):
        BBCount = int(round(self.player.money * 1.0 / (self.tableInfo["BB"] + (self.tableInfo["ante"] * self.playerCnt / 3.0 * 2.0)), 0))
        return BBCount
    
    def getSimpleHand(self):
        global tableData
        try:
            if(self.player.hand[0]['int'] > self.player.hand[1]['int']):
                firstCard = self.player.hand[0]['int']
                secondCard = self.player.hand[1]['int']
            else:
                firstCard = self.player.hand[1]['int']
                secondCard = self.player.hand[0]['int']
            sop = ''
            if(self.player.hand[0]['int'] == self.player.hand[1]['int']):
                sop = 'p'
            elif(self.player.hand[0]['suit'] == self.player.hand[1]['suit']):
                sop = 's'
            else:
                sop = 'o'
            return [firstCard, secondCard, sop]
        except:
            tableData += 'error getSimpleHand/'
    
    def checkFirstIn(self):
        if(self.tableInfo["pot"] - self.tableInfo["BB"] - self.tableInfo["SB"] - (self.tableInfo["ante"] * self.playerCnt) > self.tableInfo["BB"]):
            return False
        else:
            return True
    def getTournament(self, rawStr):
        if(rawStr.find("Tournament") != -1):
            return rawStr.split("Tournament")[1].split("Table")[0].strip()
        else:
            return ""

    def getTable(self, rawStr):
        if(rawStr.find("Table") != -1):
            return rawStr.split("Table")[1].split("-")[0].strip()
        else:
            return ""

    def getPotNumbers(self):
        cnt = 0;
        for num in self.potNums:
            pat = Pattern(num).exact()
            if(self.potAmmountRegion.exists(pat, 0)):
                self.potAmmountRegion.findAll(pat)
                mm = self.potAmmountRegion.getLastMatches()
                while mm.hasNext():
                    self.potNumsArr.append([cnt, mm.next().x])                   
            cnt += 1
        return int("".join(map(lambda obj: str(obj[0]), sorted(self.potNumsArr, key=lambda num: num[1]))))

    def getBlNumbers(self):
        cnt = 0;
        blNumsArr = []
        for num in self.blNums:
            pat = Pattern(num["img"]).exact()
            if(self.blRegion.exists(pat, 0)):
                self.blRegion.findAll(pat)
                mm = self.blRegion.getLastMatches()
                while mm.hasNext():
                    blNumsArr.append([num["val"], mm.next().x])                   
            cnt += 1
        return "".join(map(lambda obj: str(obj[0]), sorted(blNumsArr, key=lambda num: num[1])))
         
        
    def countPlayers(self):
        global tableData
        self.playerCnt = 1
        pat = Pattern(self.playerImg).exact()
        for player in self.players:
            if player['region'].exists(self.playerImg, 0):
                player['status'] = 'active'
                self.playerCnt += 1
            if player['region'].exists(self.emptySeatImg, 0):
                player['status'] = 'empty'                              
            if player['region'].exists(self.betImg1, 0):
                player['bet'] = 1
                
        self.turnData['playerCnt'] = self.playerCnt
        

    def getSittingOut(self):
        for player in self.players:
            if(player['region'].exists(self.sittingOutImg, 0)):
                    player['status'] = 'sittingOut'
                    self.sittingOut.append(player)
        return len(self.sittingOut)
        
    def getEmptySpaces(self):
        emptySeats = -1
        for player in self.players:
            if not player['region'].exists(self.playerImg, 0):
                print "empty seat nr - " + str(player["id"])
                player['status'] = 'empty'
                emptySeats += 1
        return emptySeats
    
    def getTableAvailablePositions(self):
        global positions
        global positionsCorrectionArr
        self.openPosition = [];
        playersMinus = len(self.players) - self.playerCnt
        for index in positionsCorrectionArr[playersMinus]:
            self.openPositions.append(positions[index])
        
    def getPlayersPositions(self):
        global tableData
        self.getTableAvailablePositions()
        cnt = 0
        takenPositions = []
        dealer = -1
        while len(takenPositions) < self.playerCnt:
            if(cnt >= len(self.players)):
                cnt = 0        
            player = self.players[cnt]
            if(dealer == -1):
                if(player['region'].exists(self.dealerImg, 0)):
                    dealer = cnt;
                    player['position'] = self.openPositions[0]
                    #print 'player ' + str(player['id']) + ' - ' + player['position']
                    self.openPositions[0:1] = []
                    takenPositions.append(player['position'])
                    if player['bet'] == 1:
                        self.betPositions.append(player['position'])
            else:
                if(player['status'] == 'active'):
                    player['position'] = self.openPositions[0]
                    #print 'player ' + str(player['id']) + ' - ' + player['position']
                    self.openPositions[0:1] = []
                    takenPositions.append(player['position'])
                    if player['bet'] == 1 and player['position'] != 'BB' and player['position'] != 'SB':
                        self.betPositions.append(player['position'])
            global positionsMap
            posNr = positionsMap['BB']
            for pos in self.betPositions:
                if positionsMap[pos] < posNr:
                    posNr = positionsMap[pos]
                    self.firstBet = pos
            cnt += 1
        playerCnt = self.tableLength
        positions = ''
        for player in self.players:
            if playerCnt > 0:
                positions += player['position']+'/'
                playerCnt = playerCnt - 1
            else:
                break
        return positions

    def executeAction(self, action):
        global gamesPlayed
        global gameId
        if action == 'fold':
            self.clickFold()
        elif action == 'push':
            self.clickMax()
            time.sleep(round(0.3 + 1.0 / 100 * random.randint(1, 100), 2))
            self.clickPush()
        elif action == 'random':
            self.clickButtonRandom(self.randomClickRegion, True)
        elif action == 'startNew':
            result = self.clickWindowExpand()
            if result == True:
                gamesPlayed += 1
                gameId = str(uuid.uuid4())
            else:
                gamesPlayed = 100
        else:
            self.clickFold()
                
    def clickWindowExpand(self):
        try:
            button = self.windowControlsButton.find(self.windowExpandImg)
            self.clickButtonRandom(button)
            time.sleep(round(2.3 + 1.0 / 100 * random.randint(1, 100), 2))
            return True
        except:
            return False
        
                
    def clickFold(self):
        global tableData
        button = ''
        try:
            button = self.controlsRegion.find(self.foldButton)
        except:
            try:
                button = self.controlsRegion.find(self.checkButton)
            except:
                tableData += 'error - no fold or check button found'
                try:
                    button = self.controlsRegion.find(self.sittingOutImg)
                except:
                    return
        self.clickButtonRandom(button)
        
    def clickMax(self):
        global tableData
        try:
            button = self.controlsRegion.find(self.maxButton)
            self.clickButtonRandom(button)
        except:
            print 'max button not found/'

    def clickPush(self):
        self.clickButtonRandom(self.pushButtonRegion)
        
    def clickButtonRandom(self, button, dontClick = False):
        randomX = random.randint(button.x + button.w / 10, button.x + button.w / 10 * 9)
        randomY = random.randint(button.y + button.h / 10, button.y + button.h / 10 * 9)
        randomPoint = Region(randomX, randomY, button.x / 100, button.y / 100)
        if dontClick == False:
            click(randomPoint)
        else:
            hover(randomPoint)

fileSystem = FileSystem()
turn = Turn()
gameId = str(uuid.uuid4())
print gameId
while gamesPlayed < 5:
    action = turn.waitForYourTurn()
    turn.turnData['action'] = action
    turn.executeAction(action)
    time.sleep(round(0.3 + 1.0 / 100 * random.randint(1, 100), 2))
    turn.executeAction('random')
    print tableData +" "+ str(turn.turnData['action']) +" "+ str(turn.turnData['screenshot']) +" "+ str(turn.turnData['card1']) +" "+ str(turn.turnData['card2']) +" "+ str(turn.turnData['hand']) +" "+ str(turn.turnData['firstbet']) +" "+ str(turn.turnData['playerCnt']) +" "+ str(turn.turnData['money']) +" "+ str(turn.turnData['pot']) +" "+ str(turn.turnData['SB']) +" "+ str(turn.turnData['BB']) +" "+ str(turn.turnData['ante']) +" "+ str(turn.turnData['playerPos']) +" "+ str(turn.turnData['bbs']) +" "+ str(turn.turnData['first']) +" "+ str(gameId)    
    #try:
        #response = fileSystem.logsToDatabase(str(tableData), str(turn.turnData['action']), str(turn.turnData['screenshot']), str(turn.turnData['card1']), str(turn.turnData['card2']), str(turn.turnData['hand']), str(turn.turnData['firstbet']), str(turn.turnData['playerCnt']), str(turn.turnData['money']), str(turn.turnData['pot']), str(turn.turnData['SB']), str(turn.turnData['BB']), str(turn.turnData['ante']), str(turn.turnData['playerPos']), str(turn.turnData['bbs']), str(turn.turnData['first']), str(gameId))
    #except:
        #tableData += 'error saving logs/'
    #if tableData.find('error') == -1:
        #popup(tableData.replace('/', '\n'))
    #else:
        #popError(tableData.replace('/', '\n'))
    tableData = ''
    tableScreenShot = None
    turn.cleardata()
    gamesPlayed = 7
    