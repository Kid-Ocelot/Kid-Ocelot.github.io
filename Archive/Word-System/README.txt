Made by Kid_Ocelot
Kidware Word Translating,Reciting and Management System
https://kid-ocelot.github.io

总的一个就是如下
本目录下的"Words 预设23 new.db"是预填充了Youdaoid与一些词语的db
主文件"main.py"是全英语的，开始如导入请填充完整文件名 Eg:"Words.db" 
或者选择新建数据库 Appid和Appsecret在py文件的开头注释也有

	print("Help>>有道id是去ai.youdao.com进行一个带文本翻译api的app的申请")
            print("Help>>并且将其中的appid与appsecret进行一个Main>>Youdao>>New>>那边的输入")
            print("Help>>然后主界面的Appid/secMissing就会变成Not verified")
            print("Help>>然后再到Main>>Youdao>>3:Verificate>>那边进行一个验证可用性")
            print("Help>>这样之后 Words management>>Add中的有道自动填充就可用了")
            print("Help>>并且同时main>>2的翻译也可用了")
            print("Help>>芜湖芜湖！！",end="\n\n")



            print("Help>>数据库嘛，有4个表")
            print("Help>>分别是youdao,new,prob,fin")
            print("Help>>youdao表里存了1 entry的appid与appsec")
            print("Help>>new和prob表里存了若干entries的CN,EN,value")
            print("Help>>CN代表了中文解释，EN代表英文词条，value代表在Main>>Test>里的成绩")
            print("Help>>这个value基准为0，text每错一次-1,对一次+1")
            print("Help>>fin表里存了Cn,en")
            print("Help>>为什么没有Value？ 你都背熟了还考什么试")
            print("Help>>通过Main>>Migrate也可以发现 fin表只进不出")
            print("Help>>然后在一开始导入数据库的时候 我在下面def了一个db_verification")
            print("Help>>校验表的列是不是足够 符合标准")
            print("Help>>虽然校验的有点草率 但是至少校验了（（（")
            print("Help>>主要依靠数据库提供的功能就是单词存取，测试与迁移")
            print("Help>>看心情再做一个csv导入？")
            print("Help>>这个不一定做，可能会咕咕（",end="\n\n")