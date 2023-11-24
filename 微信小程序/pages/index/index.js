// index.js
// 获取应用实例
const app = getApp()
const API = require('../../utils/api')

Page({
  data: {
    srcI: '',   
    detectPath: '',  
    result: '',  
    spent: '',  
    status:'',
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    user_id:'',
    isShow:false,
    infos:{},
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') // 如需尝试获取用户信息可改为false
  },
  clickImage(){
    this.setData({
      detectPath:'',
      result:'',
      spent:'',
      status:''
    })

    wx.chooseMedia({
      count: 1,
      mediaType: ['image','video'],
      sourceType: ['album', 'camera'],
      maxDuration: 30,
      camera: 'back',
      success: res=>{

        this.setData({
          srcI:res.tempFiles[0].tempFilePath
        })
        this.up();
      }
    })
  },
// 上传方法 ，这个name属性是最重要的属性，他对应着后端传参数的指
// 也就是 MultipartFile file 的file
  up(){
    wx.showLoading({
      title: '加载中',
      mask:false
    });
      wx.uploadFile({
      filePath: this.data.srcI,
      name: 'img',
      url: 'http://10.24.128.10:5000/upload',
      timeout: 600000, // 增加上传超时时间为60秒
      success:res=>{
        var data = JSON.parse(res.data);
        wx.hideLoading();
        console.log(data)
    // 检查数据是否成功返回
    if (data && data.status === "success") {
      // 数据成功返回，处理数据
      this.setData({
        detectPath: data.tempFilePaths[0] ? data.tempFilePaths[0] : '',
        // result: data.result ? data.result : '',
        spent: data.spent ? data.spent : '',
        status: data.status ? data.status : ''
      });
    } else {
      // 处理请求失败的情况
      wx.showToast({
        title: '请求失败，请重试',
        icon: 'none'
      });
    }
  },
  fail: err => {
    // 处理请求失败的情况
    wx.hideLoading();
    wx.showToast({
      title: '请求失败，请重试',
      icon: 'none'
    });
    console.error(err);
        
      }
    })
  },
  // 事件处理函数
  bindViewTap() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad() {
    // API.threedays().then((res)=>{
    //   console.log(res)
    // })
    // if (wx.getUserProfile) {
    //   this.setData({
    //     canIUseGetUserProfile: true
    //   })
    // }
  },
  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认，开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '展示用户信息', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        console.log(res)
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    })
  },
  getUserInfo(e) {
    // 不推荐使用getUserInfo获取用户信息，预计自2021年4月13日起，getUserInfo将不再弹出弹窗，并直接返回匿名的用户个人信息
    console.log(e)
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
