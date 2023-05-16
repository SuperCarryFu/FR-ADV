<template>
    <el-space class="jj1" direction="horizontal" alignment="center" :size="0">
        <el-card class="na" style="width: 250px; height: 530px" shadow="never">
            <div v-if="this.attack1 == '改进PGD'">
                <div align="left" style="margin: 10px">
                    <h3>攻击方法</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="attack1" placeholder="Select attack" style="width: 200px">
                        <el-option v-for="item in attacks" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>模型</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="metas" multiple placeholder="Select models" style="width: 200px">
                        <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>改进PGD参数</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="eps" placeholder="Please input eps" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="iters" placeholder="Please input iters" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-radio-group v-model="goal">
                        <el-radio :label="0" border>模仿攻击</el-radio>
                        <el-radio :label="1" border>躲避攻击</el-radio>
                    </el-radio-group>
                </div>

            </div>
        </el-card>
    </el-space>
    <el-space class="jj" direction="horizontal" alignment="center" :size="0">
        <el-card class="na" style="width: 250px; height: 530px" shadow="never">
            <div v-if="this.attack2 == '改进MIM'">
                <div align="left" style="margin: 10px">
                    <h3>攻击方法</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="attack2" placeholder="Select attack" style="width: 200px">
                        <el-option v-for="item in attacks" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>模型</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="metas" multiple placeholder="Select models" style="width: 200px">
                        <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>改进MIM参数</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="eps" placeholder="Please input eps" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="iters" placeholder="Please input iters" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="mu" placeholder="Please input mu" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-radio-group v-model="goal">
                        <el-radio :label="0" border>模仿攻击</el-radio>
                        <el-radio :label="1" border>躲避攻击</el-radio>
                    </el-radio-group>
                </div>
            </div>
        </el-card>
    </el-space>
    <el-space class="jj" direction="horizontal" alignment="center" :size="0">
        <el-card class="na" style="width: 250px; height: 530px" shadow="never">
            <div v-if="this.attack3 == '改进TIM'">
                <div align="left" style="margin: 10px">
                    <h3>攻击方法</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="attack3" placeholder="Select attack" style="width: 200px">
                        <el-option v-for="item in attacks" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>模型</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="metas" multiple placeholder="Select models" style="width: 200px">
                        <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>改进TIM参数</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="eps" placeholder="Please input eps" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="iters" placeholder="Please input iters" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="kernel_len" placeholder="Please input kernel_len" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="nsig" placeholder="Please input nsig" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-radio-group v-model="goal">
                        <el-radio :label="0" border>模仿攻击</el-radio>
                        <el-radio :label="1" border>躲避攻击</el-radio>
                    </el-radio-group>
                </div>
            </div>
        </el-card>
    </el-space>
    <el-space class="jj" direction="horizontal" alignment="center" :size="0">
        <el-card class="na" style="width: 250px; height: 530px" shadow="never">
            <div v-if="this.attack4 == '改进DIM'">
                <div align="left" style="margin: 10px">
                    <h3>攻击方法</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="attack4" placeholder="Select attack" style="width: 200px">
                        <el-option v-for="item in attacks" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>模型</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-select v-model="metas" multiple placeholder="Select models" style="width: 200px">
                        <el-option v-for="item in models" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                </div>
                <div align="left" style="margin: 10px">
                    <h3>改进DIM参数</h3>
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="eps" placeholder="Please input eps" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-input :prefix-icon="Edit" v-model="iters" placeholder="Please input iters" clearable
                        style="width: 200px" />
                </div>
                <div align="left" style="margin: 10px">
                    <el-radio-group v-model="goal">
                        <el-radio :label="0" border>模仿攻击</el-radio>
                        <el-radio :label="1" border>躲避攻击</el-radio>
                    </el-radio-group>
                </div>
            </div>
        </el-card>

    </el-space>
    <el-space class="jj" direction="horizontal" alignment="center" :size="0">
        <el-card class="na" style="width: 250px; height: 530px" shadow="never">
        <el-table :data="models" border style="width: 100%; font-size: 16px">
            <el-table-column prop="value" label="Model" />
        </el-table>
    </el-card>
    </el-space>


</template>
<script>
import { Plus } from "@element-plus/icons-vue";
import { Delete } from "@element-plus/icons-vue";
import { SwitchButton } from "@element-plus/icons-vue";
import { Edit } from "@element-plus/icons-vue";
export default {
    name: "app",

    data() {
        return {
            metas: "",
            attack1: "改进PGD",
            attack2: "改进MIM",
            attack3: "改进TIM",
            attack4: "改进DIM",
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
                    
                },
                {
                    value: "Mobilenet",
                    
                },
                {
                    value: "ArcFace",
                    
                },
                {
                    value: "MobilenetV2",
                    
                },
                {
                    value: "ShuffleNetV1",
                    
                },
                {
                    value: "ShuffleNetV2",
                    
                },
                {
                    value: "IR50-Softmax",
                    
                },
                {
                    value: "IR50-CosFace",
                    
                },
                {
                    value: "IR50-Am",
                    
                },
                {
                    value: "IR50-SphereFace",
                    
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
            tableData: [{ score1: "", score2: "", or: "" }],
            score: "",
        };
    },
    components: { Plus },
};
</script>
<style scoped>
.but /deep/ .el-page-header__left::after {
    content: none;
}

.na {
    /* float: left; */
    /* margin-right: 10px;
    margin-bottom: 10px;
    margin-left: 10px;
    margin-top: 10px; */
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
    margin-right: 5px;
    margin-bottom: 5px;
    margin-left: 5px;
    margin-top: 50px;
}

.jj1 {
    margin-right: 5px;
    margin-bottom: 5px;
    margin-left: 100px;
    margin-top: 50px;
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
  