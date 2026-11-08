<script setup lang="ts">
// 认证页公共外壳：只负责骨架和排版，不碰表单数据、校验、请求
// title 由页面传入，外壳不需要知道自己被用在登录还是注册
defineProps<{
  title: string
}>()
</script>

<template>
  <main class="auth-card">
    <header>
      <img class="brand" src="/favicon.ico" alt=""/>
      <h1>{{ title }}</h1>
    </header>

    <!-- 表单、反馈区、底部链接由各页面填进来 -->
    <slot/>
  </main>
</template>

<style scoped></style>
