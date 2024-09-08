#
# MiniTyping.py 2024/9/8
#
USE_K8X12_BDF = False
try:
    import pyttsx3
except ImportError:
    TTS = False
else:
    TTS = True
import pyxel
if USE_K8X12_BDF:
    K8X12 = pyxel.Font('./K8X12.bdf')
else:
    import kfont
W_WIDTH, W_HEIGHT = 277, 117
MSG_X, MSG_Y, MSG_WIDTH, MSG_LINE = 5, 5, W_WIDTH-10, 6
SMSG_X, SMSG_Y, SMSG_WIDTH, SMSG_HEIGHT = MSG_X+MSG_WIDTH-53, MSG_Y+4, 49, 39
IN_X, IN_Y, IN_WIDTH, IN_HEIGHT = MSG_X, 84, MSG_WIDTH, 28
SPK_X, SPK_Y = IN_X+IN_WIDTH-15, IN_Y+10
FRAME_COL = 12
NON_WORD = ' -.,\'":;/!?$0123456789'
HINT_RATE = 8
HINT_FIRST_WORD = True

class Shooting:
    def __init__(self, x, y, width, height, rate=200):
        self.sx, self.sy, self.width, self.height = x, y, width, height
        self.x1, self.y1, self.x2, self.y2, self.c = 0, 0, 0, 0, 0
        self.rate, self.state = rate, 0

    def update(self):
        if self.state==0:
            if pyxel.rndi(1, self.rate)==1:
                if pyxel.rndi(0, 1)==0:
                    self.x1 = pyxel.rndi(self.sx, self.sx+self.width//3*2)
                    self.x2 = self.x1+10+pyxel.rndi(0, 20)
                else:
                    self.x1 = pyxel.rndi(self.sx+self.width//3, self.sx+self.width)
                    self.x2 = self.x1-10-pyxel.rndi(0, 20)
                self.y1, self.y2 = 0, 10+pyxel.rndi(0, 10)
                self.c = pyxel.rndi(13, 15)
                self.state = 1
        else:
            self.x1, self.x2 = self.x1+(self.x2-self.x1)//2, self.x2+(self.x2-self.x1)//2
            self.y1, self.y2 = self.y1+(self.y2-self.y1)//2, self.y2+(self.y2-self.y1)//2
            if self.y1>self.sy+self.height:
                self.state = 0

    def draw(self):
        if self.state==1:
            pyxel.line(self.x1, self.y1, self.x2, self.y2, self.c)

class Blinking:
    def __init__(self, x, y, width, height, rate=200):
        self.sx, self.sy, self.width, self.height = x, y, width, height
        self.tx, self.ty, self.tc = 0, 0, 0
        self.rate, self.state = rate, 0

    def update(self):
        if self.state==0:
            if pyxel.rndi(1, self.rate)==1:
                self.tx = pyxel.rndi(self.sx+3, self.sx+self.width-7)
                self.ty = pyxel.rndi(self.sy+3, self.sy+self.height-7)
                self.tc = pyxel.rndi(13, 15)
                self.state = 1
        else:
            self.state += 1
            if self.state>18:
                self.state = 0

    def draw(self):
        if self.state in (1,2,3,4,17,18):
            pyxel.line(self.tx-1, self.ty, self.tx+1, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-1, self.tx, self.ty+1, self.tc)
        elif self.state in (5,6,14,15,16):
            pyxel.line(self.tx-2, self.ty, self.tx+2, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-2, self.tx, self.ty+2, self.tc)
        elif self.state in (7,8,9,10,11,12,13):
            pyxel.line(self.tx-3, self.ty, self.tx+3, self.ty, self.tc)
            pyxel.line(self.tx, self.ty-3, self.tx, self.ty+3, self.tc)

class Message:
    def __init__(self, x, y, width, line, bgcol=0, height=0):
        self.msg_x = x
        self.msg_y = y
        self.msg_width = width
        self.msg_line = line
        self.msg_frcol = 7
        self.msg_bgcol = bgcol
        if height < line*12+3:
            self.msg_height = line*12+3
        else:
            self.msg_height = height
        self.msg_scrl = 0
        self.clr()

    def clr(self):
        self.msg_str = ['']*self.msg_line
        self.msg_col = [7]*self.msg_line

    def in_message(self, new_msg, new_col=6, keep=False):
        if keep or self.msg_str[0]=='':
            self.msg_str[0] = new_msg
            self.msg_col[0] = new_col
        elif new_msg:
            for i in reversed(range(self.msg_line-1)):
                self.msg_str[i+1] = self.msg_str[i]
                self.msg_col[i+1] = self.msg_col[i]
            self.msg_str[0] = new_msg
            self.msg_col[0] = new_col
            self.msg_scrl = 12

    def draw_message(self, frcol=7):
        pyxel.rectb(self.msg_x, self.msg_y, self.msg_width, self.msg_height, frcol)
        pyxel.rect(self.msg_x+1, self.msg_y+1, self.msg_width-2, self.msg_height-2, self.msg_bgcol)
        for i in range(1, self.msg_line):
            if USE_K8X12_BDF:
                pyxel.text(self.msg_x+2, self.msg_y+2+(self.msg_line-i-1)*12+self.msg_scrl, self.msg_str[i], self.msg_col[i], K8X12)
            else:
                kfont.text(self.msg_x+2, self.msg_y+2+(self.msg_line-i-1)*12+self.msg_scrl, self.msg_str[i], self.msg_col[i])
        if self.msg_scrl==0:
            if USE_K8X12_BDF:
                pyxel.text(self.msg_x+2, self.msg_y+2+(self.msg_line-1)*12, self.msg_str[0], self.msg_col[0], K8X12)
            else:
                kfont.text(self.msg_x+2, self.msg_y+2+(self.msg_line-1)*12, self.msg_str[0], self.msg_col[0])

    def scroll(self):
        if self.msg_scrl > 0:
            self.msg_scrl -= 1
            return True
        return False

class App:
    def set_hint(self):
        ret_hint = ''
        spc = False
        for c in self.eng_org:  # Initial Letter
            if c in NON_WORD:
                spc = False
            ret_hint += ' ' if spc else c
            spc = False if c in NON_WORD else True
        for w in self.proper_noun:  # Proper Noun
            len_s, len_w = len(self.eng_org), len(w)
            for i in range(len_s-len_w+1):
                if w==self.eng_org[i:(i+len_w)]:
                    ret_hint = ret_hint[:i]+w+ret_hint[i+len(w):]
        first_word = HINT_FIRST_WORD
        find_word = False
        start_pos = end_pos = 0
        for c in self.eng_org:  # First, Random
            if c in NON_WORD:
                if find_word:
                    if first_word or pyxel.rndi(1,HINT_RATE)==1:
                        ret_hint = ret_hint[:start_pos]+self.eng_org[start_pos:end_pos]+ret_hint[end_pos:]
                    first_word = False
                    find_word = False
                    start_pos = end_pos+1
                else:
                    start_pos += 1
            else:
                if find_word:
                    end_pos += 1
                else:
                    find_word = True
                    end_pos = start_pos+1
        return ret_hint

    def hint_this_word(self):
        new_pos = self.pos+1
        while new_pos<len(self.eng_org) and not self.eng_low[new_pos] in NON_WORD:
            new_pos += 1
        new_hint = self.hint[:self.pos]+self.eng_org[self.pos:new_pos]+self.hint[new_pos:]
        return new_hint

    def set_sentence(self):
        r = pyxel.rndi(0, len(self.eng_jpn)-1)
        self.jpn = self.eng_jpn[r][1]
        self.eng_org = self.eng_jpn[r][0]
        self.eng_low = self.eng_org.lower()
        self.hint = self.set_hint()
        self.pos = 0
        self.new_pos = 0
        self.word_mistake = 0
        self.sentence_mistake = False
        self.in_pass = False

    def __init__(self):
        pyxel.init(W_WIDTH, W_HEIGHT, title='Mini Typing')
        if TTS:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)
        self.eng_jpn = []
        with open("eng_jpn.txt", "r", encoding="utf-8") as f:
            while l_eng:=f.readline().rstrip():
                l_jpn = f.readline().rstrip()
                if l_eng[0]!='#' and l_jpn[0]!='#':
                    self.eng_jpn.append([l_eng, l_jpn])
        self.proper_noun = []
        with open("proper_noun.txt", "r", encoding="utf-8") as f:
            while l:=f.readline().rstrip():
                if l[0]!='#':
                    self.proper_noun.append(l)
        self.msg = Message(MSG_X, MSG_Y, MSG_WIDTH, MSG_LINE)
        self.blink = Blinking(0, 0, W_WIDTH, W_HEIGHT, 500)
        self.shoot = Shooting(0, 0, W_WIDTH, W_HEIGHT, 1000)
        self.in_sentence = 1
        self.shake = 0
        self.total_correct = 0
        self.total_mistake = 0
        self.total_pass = 0
        pyxel.mouse(True)
        pyxel.sounds[0].set('b-1b1', '', '75', '', 4)
        pyxel.sounds[1].set('c#1c1', '', '75', '', 4)
        pyxel.sounds[2].set('e1e-1', '', '53', '', 4)
        pyxel.sounds[3].set('b1g1g1g1', '', '5753', '', 16)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.blink.update()
        self.shoot.update()
        if self.shake:
            self.shake -= 1
            return
        if self.msg.scroll():
            return
        if self.in_sentence==4:
            if TTS:
                self.engine.say(self.eng_org)
                self.engine.runAndWait()
                pyxel.mouse(True)
            self.in_sentence = 3
            return
        elif self.in_sentence==3:
            self.msg.in_message(self.jpn, 6)
            self.in_sentence = 2
            return
        elif self.in_sentence==2:
            self.msg.in_message(self.eng_org, 14 if self.sentence_mistake else 11 if self.in_pass else 10)
            self.in_sentence = 1
            return
        elif self.in_sentence==1:
            self.set_sentence()
            self.in_sentence = 0
        if self.in_pass:
            if self.pos<len(self.eng_org):
                self.pos += 1
            else:
                pyxel.stop(1)
                self.in_sentence = 4
            return
        if self.new_pos > self.pos:
            self.pos += 1
            self.shake = 1
            return
        while self.pos<len(self.eng_org) and self.eng_low[self.pos] in NON_WORD:
            self.pos += 1
            self.word_mistake = 0
        pyxel.stop(1)

        if self.pos<len(self.eng_org):
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_CTRL) or pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.KEY_ALT):  # Space,Shift,Ctrl,Alt:Ignoreor
                return
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):  # Return:Pass
                pyxel.play(1, [2], loop=True)
                self.in_pass = True
                if not self.sentence_mistake:
                    self.total_pass += 1
            elif pyxel.btnp(pyxel.KEY_TAB):  # Tab:Ward Hint
                self.hint = self.hint_this_word()
            elif pyxel.btnp(ord(self.eng_low[self.pos])):
                pyxel.play(0, [0])
                self.pos += 1
                self.word_mistake = 0
            else:
                for inputkey in range(pyxel.KEY_A, pyxel.KEY_Z+1):
                    if pyxel.btnp(inputkey):
                        pyxel.play(0, [1])
                        self.shake = 3
                        self.word_mistake += 1
                        if self.word_mistake==2:  # Mistake
                            pyxel.play(1, [2], loop=True)
                            self.new_pos = self.pos+1
                            while self.new_pos<len(self.eng_org) and not self.eng_low[self.new_pos] in NON_WORD:
                                self.new_pos += 1
                            if not self.sentence_mistake: 
                                self.total_mistake += 1
                                self.sentence_mistake = True
                        break
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) and SMSG_X<=pyxel.mouse_x<SMSG_X+SMSG_WIDTH and SMSG_Y<=pyxel.mouse_y<SMSG_Y+SMSG_HEIGHT:  # Click:Pass
                pyxel.play(1, [2], loop=True)
                self.in_pass = True
                if not self.sentence_mistake:
                    self.total_pass += 1
        else:  # Correct
            self.in_sentence = 4
            if not self.sentence_mistake:
                self.total_correct += 1
                if not TTS:
                    pyxel.play(2, [3])

    def draw(self):
        pyxel.cls(1)
        self.msg.draw_message(8 if self.shake else FRAME_COL)

        pyxel.rectb(IN_X, IN_Y, IN_WIDTH, IN_HEIGHT, 8 if self.shake else FRAME_COL)
        pyxel.rect(IN_X+1, IN_Y+1, IN_WIDTH-2, IN_HEIGHT-2, 0)
        if USE_K8X12_BDF:
            pyxel.text(IN_X+2, IN_Y+3, self.jpn, 7, K8X12)
            pyxel.text(IN_X+2, IN_Y+15, self.eng_org[:self.pos], 14 if self.sentence_mistake else 11 if self.in_pass else 10, K8X12)
        else:
            kfont.text(IN_X+2, IN_Y+3, self.jpn, 7)
            kfont.text(IN_X+2, IN_Y+15, self.eng_org[:self.pos], 14 if self.sentence_mistake else 11 if self.in_pass else 10)
        if self.pos<len(self.eng_org):
            if USE_K8X12_BDF:
                pyxel.text(IN_X+2+self.pos*4, IN_Y+15, self.hint[self.pos], 7, K8X12)
            else:
                kfont.text(IN_X+2+self.pos*4, IN_Y+15, self.hint[self.pos], 7)
        if self.pos+1<len(self.eng_org):
            if USE_K8X12_BDF:
                pyxel.text(IN_X+2+(self.pos+1)*4, IN_Y+15, self.hint[self.pos+1:], 6, K8X12)
            else:
                kfont.text(IN_X+2+(self.pos+1)*4, IN_Y+15, self.hint[self.pos+1:], 6)

        pyxel.rectb(SMSG_X, SMSG_Y, SMSG_WIDTH, SMSG_HEIGHT, 8 if self.shake else FRAME_COL)
        pyxel.rect(SMSG_X+1, SMSG_Y+1, SMSG_WIDTH-2, SMSG_HEIGHT-2, 5 if SMSG_X<=pyxel.mouse_x<SMSG_X+SMSG_WIDTH and SMSG_Y<=pyxel.mouse_y<SMSG_Y+SMSG_HEIGHT else 1)
        if USE_K8X12_BDF:
            pyxel.text(SMSG_X+3, SMSG_Y+2, f'Correct{self.total_correct:>4}', 10, K8X12)
            pyxel.text(SMSG_X+3, SMSG_Y+14, f'Mistake{self.total_mistake:>4}', 14, K8X12)
            pyxel.text(SMSG_X+3, SMSG_Y+26, f'Pass   {self.total_pass:>4}', 11, K8X12)
        else:
            kfont.text(SMSG_X+3, SMSG_Y+2, f'Correct{self.total_correct:>4}', 10)
            kfont.text(SMSG_X+3, SMSG_Y+14, f'Mistake{self.total_mistake:>4}', 14)
            kfont.text(SMSG_X+3, SMSG_Y+26, f'Pass   {self.total_pass:>4}', 11)

        if TTS and self.in_sentence==4:
            pyxel.mouse(False)
            pyxel.trib(SPK_X, SPK_Y+3, SPK_X+5, SPK_Y, SPK_X+5, SPK_Y+6, 10)
            pyxel.line(SPK_X+7, SPK_Y+2, SPK_X+7, SPK_Y+4, 10)
            pyxel.line(SPK_X+9, SPK_Y+1, SPK_X+9, SPK_Y+5, 10)
            pyxel.line(SPK_X+11, SPK_Y, SPK_X+11, SPK_Y+6, 10)

        if(self.shake):
            pyxel.camera(pyxel.rndi(-1,1), pyxel.rndi(-1,1))
        else:
            pyxel.camera()

        self.blink.draw()
        self.shoot.draw()

App()