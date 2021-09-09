# -*- coding: utf-8 -*-
from akad.ttypes import Message, Location
from random import randint

import json, ntpath

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            args[0].callback.other('You want to call the function, you must login to LINE')
    return checkLogin

class Talk(object):
    isLogin = False
    _messageReq = {}
    _unsendMessageReq = 0

    def __init__(self):
        self.isLogin = True

    """User"""

    @loggedIn
    def acquireEncryptedAccessToken(self, featureType=2):
        return self.talk.acquireEncryptedAccessToken(featureType)

    @loggedIn
    def getProfile(self):
        return self.talk.getProfile()

    @loggedIn
    def getSettings(self):
        return self.talk.getSettings()

    @loggedIn
    def getUserTicket(self):
        return self.talk.getUserTicket()

    @loggedIn
    def generateUserTicket(self):
        try:
            ticket = self.getUserTicket().id
        except:
            self.reissueUserTicket()
            ticket = self.getUserTicket().id
        return ticket

    @loggedIn
    def updateProfile(self, profileObject):
        return self.talk.updateProfile(0, profileObject)

    @loggedIn
    def updateSettings(self, settingObject):
        return self.talk.updateSettings(0, settingObject)

    @loggedIn
    def updateProfileAttribute(self, attrId, value):
        return self.talk.updateProfileAttribute(0, attrId, value)

    @loggedIn
    def updateContactSetting(self, mid, flag, value):
        return self.talk.updateContactSetting(0, mid, flag, value)

    @loggedIn
    def deleteContact(self, mid):
        return self.updateContactSetting(mid, 16, 'True')

    @loggedIn
    def renameContact(self, mid, name):
        return self.updateContactSetting(mid, 2, name)

    @loggedIn
    def addToFavoriteContactMids(self, mid):
        return self.updateContactSetting(mid, 8, 'True')

    @loggedIn
    def addToHiddenContactMids(self, mid):
        return self.updateContactSetting(mid, 4, 'True')

    """Operation"""

    @loggedIn
    def fetchOps(self, localRev, count, globalRev=0, individualRev=0):
        return self.poll.fetchOps(self, localRev, count, globalRev, individualRev)

    @loggedIn
    def fetchOperation(self, revision, count=1):
        return self.poll.fetchOperations(revision, count)

    @loggedIn
    def getLastOpRevision(self):
        return self.poll.getLastOpRevision()

    """Message"""

    @loggedIn
    def sendMessageaaaa(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
    def sendMessage(self, to, text, contentMetadata={}, contentType=0,msgid=None):
        #msg = self.generateReplyMessage(relatedMessageId)
        msg = Message()
        if 'MENTION' in contentMetadata.keys()!=None:
            try:
                msg.relatedMessageId = str(self.talk.getRecentMessagesV2(to, 10)[0].id)
                msg.relatedMessageServiceCode = 1
                msg.messageRelationType = 3
            except:
                pass
        if msgid != None:
            msg.relatedMessageId = str(msgid)
            msg.relatedMessageServiceCode = 1
            msg.messageRelationType = 3
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
    
    def adityarequestweb(self,url):
        r = requests.get("{}".format(url))
        data = r.text
        data = json.loads(data)
        return data
    
    def templatefoot(self,link,AI,AN):
        a={'AGENT_LINK': link,
        'AGENT_ICON': AI,
        'AGENT_NAME': AN}
        return a
    
    def blekedok(self,t:int=None,tt:str=None):
        r = requests.get('https://www.webtoons.com/id/genre')
        soup = BeautifulSoup(r.text,'html5lib')
        data = soup.find_all(class_='card_lst')
        datea = data[t].find_all(class_='info')
        if tt == 'data':
            return datea
        else:
            return data[t].find_all('a')
    
    def getalbum(self, to, wait):
        #to = msg.to
        ha = self.getGroupAlbum(to)
        #msg.text = self.mycmd(msg.text,wait)
        a = [a['title'] for a in ha['result']['items']];c=[a['photoCount'] for a in ha['result']['items']]
        b = '╭「 Album Group 」'
        no=0
        for i in range(len(a)):
            no+=1
            if no == len(a):b+= '\n╰{}. {} | {}'.format(no,a[i],c[i])
            else:b+= '\n│{}. {} | {}'.format(no,a[i],c[i])
        self.sendMessage(to,"{}".format(b))
    
    def adityaarchi(self,wait,sd,dd,ss,split,msg,tex,nama=[]):
        selection = MySplit(split,range(1,len(nama)+1))
        k = len(nama)//20
        for a in range(k+1):
            if a == 0:eto='╭「 '+sd+' 」─'+tex
            else:eto='├「 '+sd+' 」─'+tex
            text = ''
            mids = []
            no = a
            for i in selection.parse()[a*20 : (a+1)*20]:
                mids.append(nama[i-1])
                if dd == 'kick':self.kickoutFromGroup(ss,[nama[i-1]]);hh = ''
                if dd == 'delfriend':
                    try:self.AdityadeleteContact(nama[i-1]);hh = 'Del Friend'
                    except:hh = 'Not Friend User'
                if dd == 'delbl':
                    try:wait['blacklist'].remove(nama[i-1]);hh = 'Del BL'
                    except:hh = 'Not BL User'
                if dd == 'delwl':
                    try:wait['bots'].remove(nama[i-1]);hh = 'Del WL'
                    except:hh = 'Not WL User'
                if dd == 'delml':
                    try:wait['target'].remove(nama[i-1]);hh = 'Del ML'
                    except:hh = 'Not ML User'
                if dd == 'delblock':
                    try:self.unblockContact(nama[i-1]);hh = 'Del Block'
                    except:hh = 'Not Block User'
                if dd == '':hh = ''
                if dd == 'tag':hh = ''
                no+= 1
                if no == len(selection.parse()):text+= "\n╰{}. @! {}".format(i,hh)
                else:text+= "\n│{}. @! {}".format(i,hh)
            if dd == 'tag':self.sendMention(ss,eto+text,sd,mids)
            else:self.sendMention(msg.to,eto+text,sd,mids)
        if dd == 'tag':self.sendMessage(msg.to,'╭「 Mention 」{}\n╰Status: Success tag {} mem'.format(tex,len(nama)-(len(nama)-len(selection.parse()))))
        
    def mentionmention(self, to, wait, text, dataMid=[], pl='', ps='', pg='', pt=[]):
        arr = []
        list_text=ps
        i=0
        no=pl
        if pg == 'MENTIONALLUNSED':
            for l in dataMid:
                no+=1
                if no == len(pt):list_text+='\nâ°'+str(no)+'. @[RhyN-'+str(i)+'] '
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+'] '
                i=i+1
            text=list_text+text
        if pg == 'SIDERMES':
            for l in dataMid:
                chiya = []
            for rom in wait["lurkt"][to][dataMid[0]].items():
                chiya.append(rom[1])
            for b in chiya:
                a = '{}'.format(humanize.naturaltime(datetime.fromtimestamp(b/1000)))
                no+=1
                if no == len(pt):list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+']\nâ°    ã '+a+" ã"
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+']\nâ    ã '+a+" ã"
                i=i+1
            text=list_text+text
        if pg == 'DELFL':
            for l in dataMid:
                try:
                    self.deleteContact(l)
                    a = 'Del Friend'
                except:
                    a = 'Not Friend User'
                no+=1
                if no == len(pt):list_text+='\nâ°'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                i=i+1
            text=text+list_text
        if pg == 'DELML':
            for l in dataMid:
                if l not in settings["mimic"]["target"]:
                    a = 'Not ML User'
                else:
                    a = 'DEL ML'
                    settings["mimic"]["target"].remove(l)
                no+=1
                if no == len(pt):list_text+='\nâ°'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                else:list_text+='\nâ'+str(no)+'. @[RhyN-'+str(i)+'] '+a
                i=i+1
            text=list_text
        i=0
        for l in dataMid:
            mid=l
            name='@[RhyN-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int( ln_text.index(name) )
                line_e=(int(line_s)+int( len(name) ))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        if pg == 'MENTIONALLUNSED':self.unsendMessage(self.sendMessage(to, text, contentMetadata).id)
        else:self.sendMessage(to, text, contentMetadata)

    def deletefriendnum(self, to, wait, cmd):
        asd = self.refreshContacts()
        selection = MySplit(self.adityasplittext(cmd,'s'),range(1,len(asd)+1))
        k = len(asd)//20
        d = []
        for c in selection.parse():
            d.append(asd[int(c)-1])
        self.sendMessage(to,' ã Friendlist ã\nWaiting.....')
        for a in range(k+1):
            if a == 0:self.mentionmention(to=to,wait=wait,text='',dataMid=d[:20],pl=-0,ps='â­ã Friendlist ãâ\nâ Type: Delete Friendlist',pg='DELFL',pt=d)
            else:self.mentionmention(to=to,wait=wait,text='',dataMid=d[a*20 : (a+1)*20],pl=a*20,ps='âã Friendlist ãâ\nâ Type: Delete Friendlist',pg='DELFL',pt=d)

    def adityasuperdata(self,to,wait,text='',text1='',data=[]):
        to = to
        key = wait["setkey"].title()
        if data == []:return self.sendMessage(to, "╭───「 {} 」─\n│{}: None\n│    | Command |  \n│Add {}\n│  Key:{} add{} [@]\n│Del {}\n│  Key:{} del{} [@]\n╰──────".format(text,text,text,key,text1,text,key,text1,key,text1))
        self.datamention(to,'{}'.format(text),data)

    def deletefriendnum(self, to, wait, cmd):
        asd = self.refreshContacts()
        selection = MySplit(self.adityasplittext(cmd,'s'),range(1,len(asd)+1))
        k = len(asd)//20
        d = []
        for c in selection.parse():
            d.append(asd[int(c)-1])
        self.sendMessage(to,' 「 Friendlist 」\nWaiting.....')
        for a in range(k+1):
            if a == 0:self.mentionmention(to=to,wait=wait,text='',dataMid=d[:20],pl=-0,ps='╭「 Friendlist 」─\n├ Type: Delete Friendlist',pg='DELFL',pt=d)
            else:self.mentionmention(to=to,wait=wait,text='',dataMid=d[a*20 : (a+1)*20],pl=a*20,ps='├「 Friendlist 」─\n├ Type: Delete Friendlist',pg='DELFL',pt=d)

    def getalbum2(self, to, text, wait):
        #to = msg.to
        ha = self.getGroupAlbum(to)
        a = [a['title'] for a in ha['result']['items']];c=[a['photoCount'] for a in ha['result']['items']]
        a = text.split(' ')
        selection = MySplit(a[3],range(1,len(ha['result']['items'])+1))
        for i in selection.parse():
            try:
                b = random.randint(0,999)
                self.getImageGroupAlbum(to,ha['result']['items'][int(a[2])-1]['id'], ha['result']['items'][int(a[2])-1]['recentPhotos'][i-1]['oid'], returnAs='path', saveAs='{}.png'.format(b))
                self.sendImage(to,'{}.png'.format(b))
                os.remove('{}.png'.format(b))
            except:continue
    
    def adityasplittext(self,text,lp=''):
        separate = text.split(" ")
        if lp == '':adalah = text.replace(separate[0]+" ","")
        elif lp == 's':adalah = text.replace(separate[0]+" "+separate[1]+" ","")
        else:adalah = text.replace(separate[0]+" "+separate[1]+" "+separate[2]+" ","")
        return adalah

    @loggedIn
    def getRecentMessagesV2(self, chatId, count=1001):
        return self.talk.getRecentMessagesV2(chatId,count)

    @loggedIn
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
        
    @loggedIn
    def sendMessage1(self, messageObject):
        return self.talk.sendMessage(0,messageObject)    

    @loggedIn
    def sendMessageObject(self, msg):
        to = msg.to
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        self._msgReq += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendLocation(self, to, address, latitude, longitude, phone=None, contentMetadata={}):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = "Location by Hello World"
        msg.contentType, msg.contentMetadata = 0, contentMetadata
        location = Location()
        location.address = address
        location.phone = phone
        location.latitude = float(latitude)
        location.longitude = float(longitude)
        location.title = "Location"
        msg.location = location
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendMessageMusic(self, to, title=None, subText=None, url=None, iconurl=None, contentMetadata={}):
        """
        a : Android
        i : Ios
        """
        self.profile = self.getProfile()
        self.userTicket = self.generateUserTicket()
        title = title if title else 'LINE MUSIC'
        subText = subText if subText else self.profile.displayName
        url = url if url else 'line://ti/p/' + self.userTicket
        iconurl = iconurl if iconurl else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = title
        msg.contentType = 19
        msg.contentMetadata = {
            'text': title,
            'subText': subText,
            'a-installUrl': url,
            'i-installUrl': url,
            'a-linkUri': url,
            'i-linkUri': url,
            'linkUri': url,
            'previewUrl': iconurl,
            'type': 'mt',
            'a-packageName': 'com.spotify.music',
            'countryCode': 'ID',
            'id': 'mt000000000a6b79f9'
        }
        if contentMetadata:
            msg.contentMetadata.update(contentMetadata)
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    @loggedIn
    def sendFakeMessage(self, to, text, mids):
        contact = self.getContact(mids)
        pict = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
        name = "{}".format(contact.displayName)
        contentMetadata={"MSG_SENDER_NAME": name,"MSG_SENDER_ICON": pict}
        return self.sendMessage(to, text, contentMetadata=contentMetadata)

    @loggedIn
    def sendFakeReplyMessage(self, rynId, to, text, mids):
        contact = self.getContact(mids)
        pict = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
        name = "{}".format(contact.displayName)
        contentMetadata={"MSG_SENDER_NAME": name,"MSG_SENDER_ICON": pict}
        return self.sendReplyMessage(to, rynId, text, contentMetadata)

    @loggedIn
    def generateMessageFooter(self, title=None, link=None, iconlink=None):
        self.profile = self.getProfile()
        self.userTicket = self.generateUserTicket()
        title = title if title else self.profile.displayName
        link = link if link else 'line://ti/p/' + self.userTicket
        iconlink = iconlink if iconlink else 'https://obs.line-apps.com/os/p/%s' % self.profile.mid
        return {'AGENT_NAME': title, 'AGENT_LINK': link, 'AGENT_ICON': iconlink}

    @loggedIn
    def sendMessageWithFooter(self, to, text, title=None, link=None, iconlink=None, contentMetadata={}):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType = 0
        msg.contentMetadata = self.generateMessageFooter(title, link, iconlink)
        if contentMetadata:
            msg.contentMetadata.update(contentMetadata)
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
        
    @loggedIn
    def getRecentMessagesV2(self, messageBoxId, messagesCount=50):
        return self.talk.getRecentMessagesV2(messageBoxId, messagesCount)

    @loggedIn
    def generateReplyMessage(self, relatedMessageId):
        msg = Message()
        msg.relatedMessageServiceCode = 1
        msg.messageRelationType = 3
        msg.relatedMessageId = str(relatedMessageId)
        return msg

    @loggedIn
    def sendReplyMessage(self, relatedMessageId, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.relatedMessageServiceCode = 1
        msg.messageRelationType = 3
        msg.relatedMessageId = str(relatedMessageId)
        msg.to = to
        msg.text = text
        msg.contentType = contentType
        msg.contentMetadata = contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)
		
    @loggedIn	
    def sendMessageWithMention(self, to, text='', dataMid=[]):
        arr = []
        list_text=''
        if '[list]' in text.lower():
            i=0
            for l in dataMid:
                list_text+='\n@[list-'+str(i)+']'
                i=i+1
            text=text.replace('[list]', list_text)
        elif '[list-' in text.lower():
            text=text
        else:
            i=0
            for l in dataMid:
                list_text+=' @[list-'+str(i)+']'
                i=i+1
            text=text+list_text
        i=0
        for l in dataMid:
            mid=l
            name='@[list-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int(ln_text.index(name))
                line_e=(int(line_s)+int(len(name)))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        return self.sendMessage(to, text, contentMetadata)

    @loggedIn
    def sendReplyWithFooter(self, rynId, to, text, title=None, link=None, iconlink=None, contentMetadata={}):
        msg = self.generateReplyMessage(rynId)
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType = 0
        msg.contentMetadata = self.generateMessageFooter(title, link, iconlink)
        if contentMetadata:
            msg.contentMetadata.update(contentMetadata)
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessage(self._messageReq[to], msg)

    """ Usage:
        @to Integer
        @text String
        @dataMid List of user Mid
    """
    @loggedIn
    def sendMention(self, to, text="", mids=[]):
        arrData = ""
        arr = []
        mention = "@ryn "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            for mid in mids:
                textx += str(texts[mids.index(mid)])
                slen = len(textx)
                elen = len(textx) + 8
                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ""
            slen = len(textx)
            elen = len(textx) + 8
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        return self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

    @loggedIn
    def sendMentionV2(self, to, text="", mids=[], isUnicode=False):
        arrData = ""
        arr = []
        mention = "@rynkings__ "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            unicode = ""
            if isUnicode:
                for mid in mids:
                    unicode += str(texts[mids.index(mid)].encode('unicode-escape'))
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx) if unicode == textx else len(textx) + unicode.count('U0')
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            else:
                for mid in mids:
                    textx += str(texts[mids.index(mid)])
                    slen = len(textx)
                    elen = len(textx) + 15
                    arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                    arr.append(arrData)
                    textx += mention
            textx += str(texts[len(mids)])
        else:
            raise Exception("Invalid mention position")
        self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

    @loggedIn
    def sendReplyMention(self,RynId, to, text="", mids=[]):
        arrData = ""
        arr = []
        mention = "@rynkings__ "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            for mid in mids:
                textx += str(texts[mids.index(mid)])
                slen = len(textx)
                elen = len(textx) + 15
                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ""
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        return self.sendReplyMessage(RynId, to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

    @loggedIn
    def sendFakeMention(self, to, text="", mids=[]):
        arrData = ""
        arr = []
        mention = "@rynkings__ "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ""
            for mid in mids:
                textx += str(texts[mids.index(mid)])
                slen = len(textx)
                elen = len(textx) + 15
                arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ""
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        return self.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}'),"MSG_SENDER_NAME": "http://dl.profile.line-cdn.net/{}".format(self.getContact(arr).pictureStatus),"MSG_SENDER_ICON": "{}".format(self.getContact(arr).displayName)}, 0)
        
    @loggedIn
    def sendMessageWithMention(self, to, text='', dataMid=[]):
        arr = []
        list_text=''
        if '[list]' in text.lower():
            i=0
            for l in dataMid:
                list_text+='\n@[list-'+str(i)+']'
                i=i+1
            text=text.replace('[list]', list_text)
        elif '[list-' in text.lower():
            text=text
        else:
            i=0
            for l in dataMid:
                list_text+=' @[list-'+str(i)+']'
                i=i+1
            text=text+list_text
        i=0
        for l in dataMid:
            mid=l
            name='@[list-'+str(i)+']'
            ln_text=text.replace('\n',' ')
            if ln_text.find(name):
                line_s=int(ln_text.index(name))
                line_e=(int(line_s)+int(len(name)))
            arrData={'S': str(line_s), 'E': str(line_e), 'M': mid}
            arr.append(arrData)
            i=i+1
        contentMetadata={'MENTION':str('{"MENTIONEES":' + json.dumps(arr).replace(' ','') + '}')}
        return self.sendMessage(to, text, contentMetadata)

    @loggedIn
    def sendSticker(self, to, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendMessage(to, '', contentMetadata, 7)

    @loggedIn
    def sendReplySticker(self, RynId, to, packageId, stickerId):
        contentMetadata = {
            'STKVER': '100',
            'STKPKGID': packageId,
            'STKID': stickerId
        }
        return self.sendReplyMessage(RynId, to, '', contentMetadata, 7)
        
    @loggedIn
    def sendContact(self, to, mid):
        contentMetadata = {'mid': mid}
        return self.sendMessage(to, '', contentMetadata, 13)

    @loggedIn
    def sendReplyContact(self, RynId, to, mid):
        contentMetadata = {'mid': mid}
        return self.sendReplyMessage(RynId, to, '', contentMetadata, 13)

    @loggedIn
    def sendFakeReplyContact(self, RynId, to, mid):
        contact = self.getContact(mid)
        pict = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
        name = "{}".format(contact.displayName)
        contentMetadata={'mid' : mid,'MSG_SENDER_NAME': name,'MSG_SENDER_ICON': pict}
        return self.sendReplyMessage(RynId, to, '', contentMetadata, 13)

    @loggedIn
    def sendFakeContact(self,to, mid):
        contact = self.getContact(mid)
        pict = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
        name = "{}".format(contact.displayName)
        contentMetadata={'mid' : mid,'MSG_SENDER_NAME': name,'MSG_SENDER_ICON': pict}
        return self.sendMessage(to, '', contentMetadata, 13)

    @loggedIn
    def sendContactHP(self, to, text, nomer, nama):
        nomer = nomer
        nama = nama
        contentMetadata = {
            'vCard': 'BEGIN:VCARD\r\nVERSION:3.0\r\nPRODID:ANDROID 8.13.3 Android OS 4.4.4\r\nFN:\\{}\r\nTEL;TYPE=mobile:{}\r\nN:?;\\,\r\nEND:VCARD\r\n'.format(nama,nomer),
            'displayName': '{}'.format(nama)
        }
        return self.sendMessage(to, text, contentMetadata, 13)

    @loggedIn
    def sendGift(self, to, productId, productType):
        if productType not in ['theme','sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendMessage(to, '', contentMetadata, 9)

    @loggedIn
    def sendReplyGift(self, RynId, to, productId, productType):
        if productType not in ['theme','sticker']:
            raise Exception('Invalid productType value')
        contentMetadata = {
            'MSGTPL': str(randint(0, 12)),
            'PRDTYPE': productType.upper(),
            'STKPKGID' if productType == 'sticker' else 'PRDID': productId
        }
        return self.sendReplyMessage(RynId, to, '', contentMetadata, 9)

    @loggedIn
    def sendMessageAwaitCommit(self, to, text, contentMetadata={}, contentType=0):
        msg = Message()
        msg.to, msg._from = to, self.profile.mid
        msg.text = text
        msg.contentType, msg.contentMetadata = contentType, contentMetadata
        if to not in self._messageReq:
            self._messageReq[to] = -1
        self._messageReq[to] += 1
        return self.talk.sendMessageAwaitCommit(self._messageReq[to], msg)
       
    @loggedIn
    def unsendMessage(self, messageId):
        self._unsendMessageReq += 1
        return self.talk.unsendMessage(self._unsendMessageReq, messageId)

    @loggedIn
    def requestResendMessage(self, senderMid, messageId):
        return self.talk.requestResendMessage(0, senderMid, messageId)

    @loggedIn
    def respondResendMessage(self, receiverMid, originalMessageId, resendMessage, errorCode):
        return self.talk.respondResendMessage(0, receiverMid, originalMessageId, resendMessage, errorCode)

    @loggedIn
    def removeMessage(self, messageId):
        return self.talk.removeMessage(messageId)
    
    @loggedIn
    def removeAllMessages(self, lastMessageId):
        return self.talk.removeAllMessages(0, lastMessageId)

    @loggedIn
    def removeMessageFromMyHome(self, messageId):
        return self.talk.removeMessageFromMyHome(messageId)

    @loggedIn
    def destroyMessage(self, chatId, messageId):
        return self.talk.destroyMessage(0, chatId, messageId, sessionId)
    
    @loggedIn
    def sendChatChecked(self, consumer, messageId):
        return self.talk.sendChatChecked(0, consumer, messageId)

    @loggedIn
    def sendEvent(self, messageObject):
        return self.talk.sendEvent(0, messageObject)

    @loggedIn
    def getLastReadMessageIds(self, chatId):
        return self.talk.getLastReadMessageIds(0, chatId)

    @loggedIn
    def getPreviousMessagesV2WithReadCount(self, messageBoxId, endMessageId, messagesCount=50):
        return self.talk.getPreviousMessagesV2WithReadCount(messageBoxId, endMessageId, messagesCount)

    """Object"""

    @loggedIn
    def sendImage(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)

    @loggedIn
    def sendImageWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendImage(to, path)

    @loggedIn
    def sendReplyImage(self, rynId, to, path):
        objectId = self.sendReplyMessage(rynId, to=to, text=None, contentType = 1).id
        return self.uploadObjTalk(path=path, type='image', returnAs='bool', objId=objectId)

    @loggedIn
    def sendReplyImageWithURL(self,rynId, to, url):
        path = self.downloadFileURL(url, 'path')
        self.sendReplyImage(rynId, to, path)
        return self.deleteFile(path)

    @loggedIn
    def sendGIF(self, to, path):
        return self.uploadObjTalk(path=path, type='gif', returnAs='bool', to=to)

    @loggedIn
    def sendGIFWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendGIF(to, path)

    @loggedIn
    def sendVideo(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000','PREVIEW_URL': 'http://dl.profile.line-cdn.net/{}'.format(self.getProfile().pictureStatus)}, contentType = 2).id
        return self.uploadObjTalk(path=path, type='video', returnAs='bool', objId=objectId)

    @loggedIn
    def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendVideo(to, path)

    @loggedIn
    def sendAudio(self, to, path):
        objectId = self.sendMessage(to=to, text=None, contentType = 3).id
        return self.uploadObjTalk(path=path, type='audio', returnAs='bool', objId=objectId)

    @loggedIn
    def sendAudioWithURL(self, to, url):
        path = self.downloadFileURL(url, 'path')
        return self.sendAudio(to, path)

    @loggedIn
    def sendReplyAudio(self,rynId, to, path):
        objectId = self.sendReplyMessage(rynId, to=to, text=None, contentType = 3).id
        return self.uploadObjTalk(path=path, type='audio', returnAs='bool', objId=objectId)

    @loggedIn
    def sendReplyAudioWithURL(self,rynId, to, url):
        path = self.downloadFileURL(url, 'path')
        self.sendReplyAudio(rynId, to, path)
        return self.deleteFile(path)

    @loggedIn
    def sendFile(self, to, path, file_name=''):
        if file_name == '':
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        objectId = self.sendMessage(to=to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(file_size)}, contentType = 14).id
        return self.uploadObjTalk(path=path, type='file', returnAs='bool', objId=objectId, name=file_name)

    @loggedIn
    def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url, 'path')
        return self.sendFile(to, path, fileName)

    """Contact"""
        
    @loggedIn
    def blockContact(self, mid):
        return self.talk.blockContact(0, mid)

    @loggedIn
    def unblockContact(self, mid):
        return self.talk.unblockContact(0, mid)

    @loggedIn
    def findAndAddContactByMetaTag(self, userid, reference):
        return self.talk.findAndAddContactByMetaTag(0, userid, reference)

    @loggedIn
    def findAndAddContactsByMid(self, mid):
        return self.talk.findAndAddContactsByMid(0, mid, 0, '')

    @loggedIn
    def findAndAddContactsByEmail(self, emails=[]):
        return self.talk.findAndAddContactsByEmail(0, emails)

    @loggedIn
    def findAndAddContactsByUserid(self, userid):
        return self.talk.findAndAddContactsByUserid(0, userid)

    @loggedIn
    def findContactsByUserid(self, userid):
        return self.talk.findContactByUserid(userid)

    @loggedIn
    def findContactByTicket(self, ticketId):
        return self.talk.findContactByUserTicket(ticketId)

    @loggedIn
    def getAllContactIds(self):
        return self.talk.getAllContactIds()

    @loggedIn
    def getBlockedContactIds(self):
        return self.talk.getBlockedContactIds()

    @loggedIn
    def getContact(self, mid):
        return self.talk.getContact(mid)

    @loggedIn
    def getContacts(self, midlist):
        return self.talk.getContacts(midlist)

    @loggedIn
    def getFavoriteMids(self):
        return self.talk.getFavoriteMids()

    @loggedIn
    def getHiddenContactMids(self):
        return self.talk.getHiddenContactMids()

    @loggedIn
    def tryFriendRequest(self, midOrEMid, friendRequestParams, method=1):
        return self.talk.tryFriendRequest(midOrEMid, method, friendRequestParams)

    @loggedIn
    def makeUserAddMyselfAsContact(self, contactOwnerMid):
        return self.talk.makeUserAddMyselfAsContact(contactOwnerMid)

    @loggedIn
    def getContactWithFriendRequestStatus(self, id):
        return self.talk.getContactWithFriendRequestStatus(id)

    @loggedIn
    def reissueUserTicket(self, expirationTime=100, maxUseCount=100):
        return self.talk.reissueUserTicket(expirationTime, maxUseCount)
    
    @loggedIn
    def cloneContactProfile(self, mid, channel):
        contact = self.getContact(mid)
        path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
        path = self.downloadFileURL(path)
        self.updateProfilePicture(path)
        profile = self.profile
        profile.displayName = contact.displayName
        profile.statusMessage = contact.statusMessage
        if channel.getProfileCoverId(mid) is not None:
            channel.updateProfileCoverById(channel.getProfileCoverId(mid))
        return self.updateProfile(profile)

    """Group"""

    @loggedIn
    def getChatRoomAnnouncementsBulk(self, chatRoomMids):
        return self.talk.getChatRoomAnnouncementsBulk(chatRoomMids)

    @loggedIn
    def getChatRoomAnnouncements(self, chatRoomMid):
        return self.talk.getChatRoomAnnouncements(chatRoomMid)

    @loggedIn
    def createChatRoomAnnouncement(self, chatRoomMid, type, contents):
        return self.talk.createChatRoomAnnouncement(0, chatRoomMid, type, contents)

    @loggedIn
    def removeChatRoomAnnouncement(self, chatRoomMid, announcementSeq):
        return self.talk.removeChatRoomAnnouncement(0, chatRoomMid, announcementSeq)

    @loggedIn
    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    
    @loggedIn
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)

    @loggedIn
    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(0, groupId)

    @loggedIn
    def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.talk.acceptGroupInvitationByTicket(0, groupId, ticketId)

    @loggedIn
    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(0, groupId, contactIds)

    @loggedIn
    def createGroup(self, name, midlist):
        return self.talk.createGroup(0, name, midlist)
    @loggedIn
    def createPostGroup(self, cmd, midlist):
        return self.talk.createPostGroup(0, cmd, midlist)

    @loggedIn
    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)

    @loggedIn
    def getGroups(self, groupIds):
        return self.talk.getGroups(groupIds)

    @loggedIn
    def getGroupsV2(self, groupIds):
        return self.talk.getGroupsV2(groupIds)

    @loggedIn
    def getCompactGroup(self, groupId):
        return self.talk.getCompactGroup(groupId)

    @loggedIn
    def getCompactRoom(self, roomId):
        return self.talk.getCompactRoom(roomId)

    @loggedIn
    def getGroupIdsByName(self, groupName):
        gIds = []
        for gId in self.getGroupIdsJoined():
            g = self.getCompactGroup(gId)
            if groupName in g.name:
                gIds.append(gId)
        return gIds

    @loggedIn
    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()

    @loggedIn
    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()

    @loggedIn
    def updateGroupPreferenceAttribute(self, groupMid, updatedAttrs):
        return self.talk.updateGroupPreferenceAttribute(0, groupMid, updatedAttrs)

    @loggedIn
    def inviteIntoGroup(self, groupId, midlist):
        return self.talk.inviteIntoGroup(0, groupId, midlist)

    @loggedIn
    def kickoutFromGroup(self, groupId, midlist):
        return self.talk.kickoutFromGroup(0, groupId, midlist)

    @loggedIn
    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(0, groupId)

    @loggedIn
    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(0, groupId)

    @loggedIn
    def reissueGroupTicket(self, groupId):
        return self.talk.reissueGroupTicket(groupId)

    @loggedIn
    def updateGroup(self, groupObject):
        return self.talk.updateGroup(0, groupObject)

    """Room"""

    @loggedIn
    def createRoom(self, midlist):
        return self.talk.createRoom(0, midlist)

    @loggedIn
    def getRoom(self, roomId):
        return self.talk.getRoom(roomId)

    @loggedIn
    def inviteIntoRoom(self, roomId, midlist):
        return self.talk.inviteIntoRoom(0, roomId, midlist)

    @loggedIn
    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(0, roomId)

    """Call"""
        
    @loggedIn
    def acquireCallTalkRoute(self, to):
        return self.talk.acquireCallRoute(to)
    
    """Report"""

    @loggedIn
    def reportSpam(self, chatMid, memberMids=[], spammerReasons=[], senderMids=[], spamMessageIds=[], spamMessages=[]):
        return self.talk.reportSpam(chatMid, memberMids, spammerReasons, senderMids, spamMessageIds, spamMessages)
        
    @loggedIn
    def reportSpammer(self, spammerMid, spammerReasons=[], spamMessageIds=[]):
        return self.talk.reportSpammer(spammerMid, spammerReasons, spamMessageIds)