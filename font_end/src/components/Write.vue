<template>
  <div class="write-container">
    <h2>Continue Writing Your Novel</h2>
    <textarea placeholder="..." v-model="content"></textarea>
    <button @click="save">Save</button>
  </div>
</template>

<script>
export default {
  name: 'Write',
  data() {
    return {
      content: '',
    };
  },
  methods: {
    save() {
      console.log('Saving content', this.content);
      // Add your save logic here
    },
  },
};
</script>

<style>
.write-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #fff;
}
textarea {
  width: 100%;
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
