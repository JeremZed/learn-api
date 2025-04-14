<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'


const route = useRoute()
const router = useRouter()
const { t } = useI18n();

function resolveLabel(meta, currentRoute) {
  if (!meta || !meta.breadcrumb) return null

  // Si la valeur est une fonction, on l'appelle avec la route
  if (typeof meta.breadcrumb === 'function') {
    return meta.breadcrumb(currentRoute)
  }

  // Sinon on essaie de traduire, ou on revoie la string brute
  return t(meta.breadcrumb) || meta.breadcrumb
}

function buildBreadcrumbTrail(currentRoute) {
  const breadcrumbTrail = []

  let routeName = currentRoute.name

  while (routeName) {
    const routeRecord = router.getRoutes().find(r => r.name === routeName)
    if (!routeRecord) break

    const label = resolveLabel(routeRecord.meta, currentRoute)
    if (label) {
      breadcrumbTrail.unshift({
        name: routeRecord.name,
        label,
        path: routeRecord.path.includes(':') ? router.resolve({ name: routeRecord.name, params: currentRoute.params }).path : routeRecord.path
      })
    }

    routeName = routeRecord.meta?.parent
  }

  return breadcrumbTrail
}

const breadcrumbItems = computed(() => buildBreadcrumbTrail(route))
</script>

<template>
    <nav class="breadcrumb" v-if="breadcrumbItems.length > 0">
    <ul>
      <li>
        <router-link :to="{name:'home'}" class="link-parent">{{ $t('breadcrumb_home') }}</router-link>
      </li>
      <li v-for="(item, index) in breadcrumbItems" :key="item.name">
        <span v-if="index === breadcrumbItems.length - 1" class="link-current">{{ item.label }}</span>
        <router-link v-else :to="item.path" class="link-parent" >{{ item.label }}</router-link>
      </li>
    </ul>
  </nav>
</template>