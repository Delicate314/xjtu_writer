<template>
  <div>
    <h2>XJTU小说续写家</h2>
    <textarea placeholder="续写你的小说~" v-model="content"></textarea>
    <button @click="save">提交</button>
  </div>
</template>

<script>
export default {
  name: 'WriteView',
  data() {
    return {
      content: '',
    };
  },
  methods: {
    save() {
      console.log('提交', this.content);
      // Add your save logic here
    },
  },
};
</script>

<style>
textarea {
  width: 300px;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
