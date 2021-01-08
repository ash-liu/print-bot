//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello ',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    filePaths: ''
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },

  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  getFile: function() {
    var tempFilePaths = '';
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      success (res) {
        tempFilePaths = res.tempFiles;
        wx.uploadFile({
          url: 'https://wx.ashliu.com/upload.php', //仅为示例，非真实的接口地址
          filePath: tempFilePaths[0]["path"],
          name: 'file',
          formData: {
            'file_name': tempFilePaths[0]["name"]
          },
          success (res){
            const data = res.data;
            console.log(tempFilePaths[0]);
            console.log(res);
            //do something
            wx.showToast({
              title: '投递成功',
              icon: 'success',
              duration: 2000
            })
          },
          fail (error){
            console.log(tempFilePaths[0])
            console.log(error)
            wx.showToast({
              title: "失败",
              icon: 'fail',
              duration: 2000
            })
          }
        })
      }
    });
  }
})
