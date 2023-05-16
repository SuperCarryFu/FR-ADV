<template>
  <el-dialog
    title="对抗样本生成中"
    v-model="dialogTableVisible"
    :show-close="false"
    :center="true"
  >
    <el-progress
      :percentage="100"
      status="success"
      :indeterminate="true"
      :duration="5"
    />
    <span>请耐心等待~</span>
  </el-dialog>
  <el-card class="na" style="width: 700px; height: 530px" shadow="never">
    <el-space class="jjjj" direction="vertical" alignment="center" :size="30">
      <el-space class="jj" direction="horizontal" alignment="center" :size="30">
        <el-upload
          class="avatar-uploader"
          ref="upload"
          action="action"
          :show-file-list="false"
          :http-request="uploadFile_1"
        >
          <img v-if="imageUrl_1" :src="imageUrl_1" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus />干净样本</el-icon>
        </el-upload>
        <el-upload
          class="avatar-uploader"
          ref="upload"
          action="action"
          :show-file-list="false"
          :http-request="uploadFile_2"
        >
          <img v-if="imageUrl_2" :src="imageUrl_2" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus />目标图像</el-icon>
        </el-upload>
        <div class="xx" @click="getPic">
          <img v-if="picurl" :src="picurl" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus />对抗样本</el-icon>
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
        <el-button
          :icon="SwitchButton"
          @click="getScore"
          style="width: 120px; height: 20px; font-size: 15px"
          >测试</el-button
        >
      </el-space>
    </el-space>
    <el-page-header class="but" @back="goBack" />
  </el-card>

  <el-card class="f" style="width: 300px; height: 530px" shadow="never">
    <!-- PGD -->
    <div v-if="this.attack == '改进PGD'">
      <div align="left" style="margin: 10px">
        <h3>攻击方法</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="attack"
          placeholder="Select attack"
          style="width: 200px"
        >
          <el-option
            v-for="item in attacks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>模型</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="metas"
          multiple
          placeholder="Select models"
          style="width: 200px"
        >
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>改进PGD参数</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="eps"
          placeholder="Please input eps"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="iters"
          placeholder="Please input iters"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="goal">
          <el-radio :label="0" border>模拟攻击</el-radio>
          <el-radio :label="1" border>躲避攻击</el-radio>
        </el-radio-group>
      </div>
      <!-- <div align="left" style="margin: 10px">
        <el-radio-group v-model="metric">
          <el-radio :label="0" border>L2</el-radio>
          <el-radio :label="1" border>L∞</el-radio>
        </el-radio-group>
      </div> -->
    </div>
    <!-- CIM参数 -->
    <!-- <div v-if="this.attack == '改进CIM'">
      <div align="left" style="margin: 10px">
        <h3>攻击算法</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="attack"
          placeholder="Select attack"
          style="width: 200px"
        >
          <el-option
            v-for="item in attacks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>模型</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="metas"
          multiple
          placeholder="Select models"
          style="width: 200px"
        >
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>改进CIM参数</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="eps"
          placeholder="Please input eps"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="iters"
          placeholder="Please input iters"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="length"
          placeholder="Please input length"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="goal">
          <el-radio :label="0" border>模拟攻击</el-radio>
          <el-radio :label="1" border>躲避攻击</el-radio>
        </el-radio-group>
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="metric">
          <el-radio :label="0" border>L2</el-radio>
          <el-radio :label="1" border>L∞</el-radio>
        </el-radio-group>
      </div>
    </div> -->
    <!-- DIM参数 -->
    <div v-if="this.attack == '改进DIM'">
      <div align="left" style="margin: 10px">
        <h3>攻击算法</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="attack"
          placeholder="Select attack"
          style="width: 200px"
        >
          <el-option
            v-for="item in attacks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>模型</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="metas"
          multiple
          placeholder="Select models"
          style="width: 200px"
        >
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>改进DIM参数</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="eps"
          placeholder="Please input eps"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="iters"
          placeholder="Please input iters"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="goal">
          <el-radio :label="0" border>模拟攻击</el-radio>
          <el-radio :label="1" border>躲避攻击</el-radio>
        </el-radio-group>
      </div>
      <!-- <div align="left" style="margin: 10px">
        <el-radio-group v-model="metric">
          <el-radio :label="0" border>L2</el-radio>
          <el-radio :label="1" border>L∞</el-radio>
        </el-radio-group>
      </div> -->
    </div>
    <!-- MIM参数 -->
    <div v-if="this.attack == '改进MIM'">
      <div align="left" style="margin: 10px">
        <h3>攻击算法</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="attack"
          placeholder="Select attack"
          style="width: 200px"
        >
          <el-option
            v-for="item in attacks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>模型</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="metas"
          multiple
          placeholder="Select models"
          style="width: 200px"
        >
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>改进MIM参数</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="eps"
          placeholder="Please input eps"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="iters"
          placeholder="Please input iters"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="mu"
          placeholder="Please input mu"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="goal">
          <el-radio :label="0" border>模拟攻击</el-radio>
          <el-radio :label="1" border>躲避攻击</el-radio>
        </el-radio-group>
      </div>
      <!-- <div align="left" style="margin: 10px">
        <el-radio-group v-model="metric">
          <el-radio :label="0" border>L2</el-radio>
          <el-radio :label="1" border>L∞</el-radio>
        </el-radio-group>
      </div> -->
    </div>
    <!-- TIM参数 -->
    <div v-if="this.attack == '改进TIM'">
      <div align="left" style="margin: 10px">
        <h3>攻击算法</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="attack"
          placeholder="Select attack"
          style="width: 200px"
        >
          <el-option
            v-for="item in attacks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>模型</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-select
          v-model="metas"
          multiple
          placeholder="Select models"
          style="width: 200px"
        >
          <el-option
            v-for="item in models"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div align="left" style="margin: 10px">
        <h3>改进TIM参数</h3>
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="eps"
          placeholder="Please input eps"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="iters"
          placeholder="Please input iters"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="kernel_len"
          placeholder="Please input kernel_len"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-input
          :prefix-icon="Edit"
          v-model="nsig"
          placeholder="Please input nsig"
          clearable
          style="width: 200px"
        />
      </div>
      <div align="left" style="margin: 10px">
        <el-radio-group v-model="goal">
          <el-radio :label="0" border>模拟攻击</el-radio>
          <el-radio :label="1" border>躲避攻击</el-radio>
        </el-radio-group>
      </div>
      <!-- <div align="left" style="margin: 10px">
        <el-radio-group v-model="metric">
          <el-radio :label="0" border>L2</el-radio>
          <el-radio :label="1" border>L∞</el-radio>
        </el-radio-group>
      </div> -->
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
      metas: "",
      attack: "改进PGD",
      attacks: [
        // {
        //   value: "改进CIM",
        //   label: "改进CIM",
        // },
        {
          value: "改进DIM",
          label: "改进DIM",
        },
        {
          value: "改进MIM",
          label: "改进MIM",
        },
        {
          value: "改进PGD",
          label: "改进PGD",
        },
        {
          value: "改进TIM",
          label: "改进TIM",
        },
      ],
      dialogTableVisible: false,
      imageUrl_1: "",
      imageUrl_2: "",
      Delete,
      SwitchButton,
      Edit,
      picurl: "",
      eps: "",
      goal: "",
      metric: "",
      model: "",
      models: [
        {
          value: "MobileFace",
          label: "MobileFace",
        },
        {
          value: "Mobilenet",
          label: "Mobilenet",
        },
        {
          value: "ArcFace",
          label: "ArcFace",
        },
        {
          value: "MobilenetV2",
          label: "MobilenetV2",
        },
        {
          value: "ShuffleNet_V1",
          label: "ShuffleNet_V1",
        },
        {
          value: "ShuffleNet_V2",
          label: "ShuffleNet_V2",
        },
        {
          value: "IR50-Softmax",
          label: "IR50-Softmax",
        },
        {
          value: "IR50-CosFace",
          label: "IR50-CosFace",
        },
        {
          value: "IR50-ArcFace",
          label: "IR50-ArcFace",
        },
        {
          value: "IR50-SphereFace",
          label: "IR50-SphereFace",
        },{
          value:"All",
          label:"All"
        }
      ],
      // attack: "FGSM",
      // attacks: [
      //   {
      //     value: "FGSM",
      //     label: "FGSM",
      //   },
      //   {
      //     value: "CIM",
      //     label: "CIM",
      //   },
      //   {
      //     value: "DIM",
      //     label: "DIM",
      //   },
      //   {
      //     value: "MIM",
      //     label: "MIM",
      //   },
      //   {
      //     value: "PGD",
      //     label: "PGD",
      //   },
      //   {
      //     value: "TIM",
      //     label: "TIM",
      //   },
      // ],
      iters: "",
      mu: "",
      length: "",
      kernel_len: "",
      nsig: "",
      tableData: [{ score1: "",score2:"", or: "" }],
      score: "",
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

      const res = await axios.post("http://127.0.0.1:5000/upload?src=0", form);
      console.log(res);
      this.imageUrl_1 = res.data;
    },
    async uploadFile_2(params) {
      let form = new FormData();
      form.append("file", params.file);

      const res = await axios.post("http://127.0.0.1:5000/upload?src=1", form);
      console.log(res);
      this.imageUrl_2 = res.data;
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
    fuju(){
      console.log(this.metas)
    },
    //从服务器获取图片
    getPic() {
      this.dialogTableVisible = true;
      var that = this;
      axios({
        method: "get",
        url:
          "http://127.0.0.1:5000/getMeta?eps=" +
          this.eps +
          "&goal=" +
          this.goal +
          "&metric=" +
          this.metric +
          "&models=" +
          this.metas +
          "&iters=" +
          this.iters+
          "&attack="+
          this.attack+ 
          "&length=" +
          this.length +
          "&mu=" +
          this.mu +
          "&kernel_len=" +
          this.kernel_len +
          "&nsig=" +
          this.nsig,
        responseType: "arraybuffer", // 最为关键
      }).then(function (response) {
        that.dialogTableVisible = false;
        that.picurl =
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
