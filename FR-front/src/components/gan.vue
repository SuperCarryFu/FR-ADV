<template>
  <el-dialog title="对抗样本生成中" v-model="dialogTableVisible" :show-close="false" :center="true">
    <el-progress :percentage="100" status="success" :indeterminate="true" :duration="5" />
    <span>请耐心等待~</span>
  </el-dialog>
  <el-card class="na" style="width: 700px; height: 530px" shadow="never">
    <el-space class="jjjj" direction="vertical" alignment="center" :size="30">
      <el-space class="jj" direction="horizontal" alignment="center" :size="30">
        <el-upload class="avatar-uploader" :show-file-list="false" :http-request="uploadFile_1">
          
          <img v-if="imageUrl_1" :src="imageUrl_1" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
            干净样本
          </el-icon>
        </el-upload>
        
        <div class="xx" @click="gettar">
          <img v-if="pictar" :src="pictar" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
            目标图像
          </el-icon>
        </div>
        <div class="xx" @click="getPic">
          <img v-if="picurl" :src="picurl" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon">
            <Plus />
            对抗样本
          </el-icon>
        </div>
      </el-space>
      <el-space class="jjj" direction="vertical" alignment="center" :size="30">
        <el-table :data="tableData" style="width: 100%" size="medium">
          <!-- <el-table-column prop="score" label="Score" width="180" /> -->
          <el-table-column label="Score(0-100)" width="100" align="center">
            <el-table-column prop="score2" label="扰动前" width="180"  align="center">
            </el-table-column>
            <el-table-column prop="score1" label="扰动后" width="180" align="center">
            </el-table-column>
          </el-table-column>
          <el-table-column prop="or" label="Yes or No" width="180" align="center" />
        </el-table>
        <el-button :icon="SwitchButton" @click="getScore1"
          style="width: 120px; height: 20px; font-size: 15px">测试</el-button>
      </el-space>
    </el-space>
    <!-- <el-space class="but" direction="vertical" :size="30"> -->
    <el-page-header class="but" @back="goBack"/>

    <!-- </el-space> -->
  </el-card>

  <el-card class="f" style="width: 300px; height: 530px" shadow="never">
    <div align="left" style="margin: 10px">
      <h3>模型</h3>
    </div>
    <div align="left" style="margin: 10px">
      <el-select v-model="attack" placeholder="Select model" style="width: 200px">
        <el-option v-for="item in attacks" :key="item.value" :label="item.label" :value="item.value" @click="gettar" />
      </el-select>
    </div>


  </el-card>
</template>
<script>
import { Plus } from "@element-plus/icons-vue";
import { Delete } from "@element-plus/icons-vue";
import { SwitchButton } from "@element-plus/icons-vue";
import { Edit } from "@element-plus/icons-vue";
import axios from "axios";
export default {
  name: "app",

  data() {
    return {
      dialogTableVisible: false,
      imageUrl_1: "",
      imageUrl_2: "",
      Delete,
      SwitchButton,
      Edit,
      picurl: "",
      pictar: "",
      attack: "",
      attacks: [
        {
          value: "模型1",
          label: "模型1",
        },
        {
          value: "模型2",
          label: "模型2",
        },
        {
          value: "模型3",
          label: "模型3",
        },
        {
          value: "模型4",
          label: "模型4",
        },
        {
          value: "模型5",
          label: "模型5",
        },
        {
          value: "模型6",
          label: "模型6",
        },
        {
          value: "模型7",
          label: "模型7",
        },
        {
          value: "模型8",
          label: "模型8",
        }, {
          value: "模型9",
          label: "模型9",
        },
        {
          value: "模型10",
          label: "模型10",
        },
      ],
      tableData: [{ score1: "",score2:"", or: "" }],
      // score1: "",
      // score2: "",
    };
  },

  methods: {
    goBack() {
      this.$router.push("/home");
    },
    cc() {
      this.dialogTableVisible = true;
      setTimeout(() => {
        this.dialogTableVisible = false;
      }, 5000);
    },
    // 上传图片
    async uploadFile_1(params) {
      let form = new FormData();
      form.append("file", params.file);

      const res = await axios.post("http://127.0.0.1:5000/uploadGAN?src=0", form);
      console.log(res);
      this.imageUrl_1 = res.data;
    },
    //删除图片
    del_1() {
      axios.get("http://127.0.0.1:5000/delete_1", {}).then((res) => {
        this.imageUrl_1 = res.data.img;
      });
    },
    del_2() {
      axios.get("http://127.0.0.1:5000/delete_2", {}).then((res) => {
        this.imageUrl_2 = res.data.img;
      });
    },
    //从服务器获取图片
    getPic() {
      this.dialogTableVisible = true;
      var that = this;
      axios({
        method: "get",
        url:
          "http://127.0.0.1:5000/getPic?attack=" +
          this.attack,
        responseType: "arraybuffer", // 最为关键
      }).then(function (response) {
        that.dialogTableVisible = false;
        that.picurl =
          "data:image/png;base64," + that.arrayBufferToBase64(response.data);
      });
    },
    gettar() {
      // this.dialogTableVisible = true;
      var that = this;
      axios({
        method: "get",
        url:
          "http://127.0.0.1:5000/gettar?attack=" +
          this.attack,
        responseType: "arraybuffer", // 最为关键
      }).then(function (response) {
        // that.dialogTableVisible = false;
        that.pictar =
          "data:image/png;base64," + that.arrayBufferToBase64(response.data);
      });
    },
    // ArrayBuffer转为base64字符串
    arrayBufferToBase64(buffer) {
      //第一步，将ArrayBuffer转为二进制字符串
      var binary = "";
      var bytes = new Uint8Array(buffer);
      var len = bytes.byteLength;
      for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
      }
      //将二进制字符串转为base64字符串
      return window.btoa(binary);
    },
    getScore() {
      axios.get("http://127.0.0.1:5000/contrast", {}).then((res) => {
        this.tableData[0].score1 = res.data.score1;
        this.tableData[0].score2 = res.data.score2;
        if (this.tableData[0].score1 >= 50) {
          this.tableData[0].or = "Yes";
        } else {
          this.tableData[0].or = "No";
        }
      });
      // console.log(this.tableData[0].score);
    },
    getScore1() {
      axios.get("http://127.0.0.1:5000/contrast1?attack=" +
        this.attack, {}).then((res) => {
          this.tableData[0].score1 = res.data.score1;
          this.tableData[0].score2 = res.data.score2;
          if (this.tableData[0].score1 >= 50) {
            this.tableData[0].or = "Yes";
          } else {
            this.tableData[0].or = "No";
          }
        });
      // console.log(this.tableData[0].score);
    },
  },
  components: { Plus },
};
</script>
<style scoped>
.but /deep/ .el-page-header__left::after{
  content: none;
}
.na {
  float: left;
  margin-right: 20px;
  margin-bottom: 20px;
  margin-left: 100px;
  margin-top: 30px;
}

.f {
  float: right;
  margin-right: 100px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-top: 30px;
}

.xx {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
}

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}

.jj {
  margin-right: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
  margin-top: 20px;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
