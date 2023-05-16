<template>
  <div class="app-container" :style="backgroundDiv" >
  <el-container>
    <el-container>
      <el-header>
        <div class="b">
          <iframe width="250" scrolling="no" height="100" frameborder="0" allowtransparency="true"
            src="https://i.tianqi.com?c=code&id=12&icon=1&py=dalian&num=1&site=20"></iframe>
        </div>
      </el-header>
      <el-main>
        <!-- <div class="front">人脸识别系统的对抗样本制作</div> -->

        <br>
        <br>
        <br>
        <br>
        <div class="front">人脸识别对抗样本生成系统</div>
        <br />
        <br>
        <br>
      <br>
      <br>
        <br>
      <br>
        <div class="a">
          <el-row :gutter="0">
            <el-col :span="12">
              <!-- <el-link :underline="false" @click="link1">基于GAN的对抗攻击 </el-link> -->
              <el-button type="primary" size="large" plain @click="link1" style="font-size: 35px;height:60px">基于GAN的对抗样本生成</el-button>
            </el-col>
            <el-col :span="12">
              <!-- <el-link :underline="false" @click="link2">基于梯度的对抗攻击</el-link> -->
              <el-button type="primary" size="large" plain @click="link2" style="font-size: 35px;height:60px">基于梯度的对抗样本生成</el-button>
              <!-- style="width: 300px; height:100px" -->
            </el-col>
          </el-row>
        </div>
        
        <!-- <br>
        <br>
        <br>
        <p class="f"> -->
          <!-- <el-carousel :interval="4000" type="card" height="250px">
            <el-carousel-item v-for="item in imagebox" :key="item.id">
              <img :src="item.idView" class="image" />
            </el-carousel-item>
          </el-carousel> -->
          <!-- <el-carousel :interval="4000" height="250px">
            <el-carousel-item v-for="item in imagebox" :key="item.id">
              <img :src="item.idView" class="image" />
            </el-carousel-item>

          </el-carousel>
        </p>
        <br> -->
      </el-main>
      <!-- <el-footer> 制作人：SuperCarry </el-footer> -->
    </el-container>
  </el-container>
  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      imagebox: [
        { id: 0, idView: require('../assets/imagebox/88.png') },
        { id: 1, idView: require('../assets/imagebox/22.png') },
        { id: 2, idView: require('../assets/imagebox/33.png') },
        { id: 3, idView: require('../assets/imagebox/44.png') },
        { id: 4, idView: require('../assets/imagebox/55.png') },
        { id: 5, idView: require('../assets/imagebox/66.png') },
        { id: 6, idView: require('../assets/imagebox/77.png') },
      ],
      backgroundDiv: {
        backgroundImage: 'url(' + require('@/assets/imagebox/R-C.jpg') + ')',
        backgroundRepeat: 'no-repeat',
        backgroundSize: '100% 100%'
      }

    };
  },
  methods: {
    link1() {
      this.$router.push("/gan");
    },
    link2() {
      this.$router.push("/meta");
    },
    link3() {
      this.$router.push("/test");
    },
  },
};
</script>

<style scoped>
.f {
  width: 800px;
  margin: 0 auto;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.b {
  float: right;
  margin-right: 30px;
  margin-bottom: 30px;
  margin-left: 550px;
  margin-top: 40px;
}

.el-container {
  height: 100%;
}

.el-link {
  font-size: 25px;
}

.el-header,
.el-footer {
  /* background-color: #b3c0d1; */
  color: #333;
  text-align: center;
  line-height: 50px;
  text-align: right;
  font-size: 12px;
  height: 50px;
}

.el-main {
  /* background-color: #e9eef3; */
  color: #333;
  text-align: center;
  /* line-height: 160px; */
}

/* .a { */
/* display: flex; */
/* } */
.front {
  font-size: 50px;
  font-weight: bold;
  font-weight: 400;
}

.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
  text-align: center;
  font-size: 20px;
}

.c {
  text-align: center;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.el-carousel {
  width: 800px;
  /* position: absolute; */
  /* left: 50%;
    top: 50%; */
  /* margin: -50px 0 0 -50px; */
}

.app-container {
  height: 100%;
  width: 100%;
}
</style>

<style>
html,
body,
#app {
  height: 100%;
  margin: 0px;
  padding: 0px;
}
</style>
