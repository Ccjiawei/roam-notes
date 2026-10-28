<script setup>
defineProps({place:Object,saved:Boolean});
defineEmits(['save']);
</script>
<template>
<article class="place-card">
  <div class="card-photo"><a :href="`#place/${place.id}`" :aria-label="`查看${place.name}详情`"><img :src="place.image" :alt="place.name" loading="lazy" width="640" height="480"/></a><span class="photo-tag">{{place.category}}</span><button class="save-icon" :class="{saved}" :aria-label="`${saved?'取消收藏':'收藏'}${place.name}`" :aria-pressed="saved" @click="$emit('save',place.id)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h12v17l-6-4-6 4z"/></svg></button></div>
  <a class="card-text" :href="`#place/${place.id}`"><span class="eyebrow location">{{place.country}}<span>·</span>{{place.province}}</span><div class="card-title"><h3>{{place.name}}</h3><span aria-hidden="true">↗</span></div><p>{{place.subtitle}}</p><div class="card-tags"><span v-for="tag in place.tags" :key="tag">{{tag}}</span></div></a>
</article>
</template>
