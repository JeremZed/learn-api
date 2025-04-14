<script setup>
import { useI18n } from "vue-i18n";
import { faLock, faCircleInfo, faReceipt } from '@fortawesome/free-solid-svg-icons';

import Card from "@/components/Card.vue"

const { t } = useI18n();
</script>

<template>
    <div class="p-account">
      <h1>{{ $t("page_account_title") }} </h1>

      <div class="row">
        <div class="col-1"></div>
        <div class="col-5">
            <Card
                :title="t('title_security')"
                :description="t('description_security')"
                :icon="faLock"
                :actions="[{to : 'security', label : t('to_access') }]"
              >
            </Card>
        </div>
        <div class="col-5">
          <Card
                :title="t('title_my_informations')"
                :description="t('description_my_informations')"
                :icon="faCircleInfo"
                :actions="[{to : 'information', label : t('to_access') }]"
              >
          </Card>
        </div>
        <div class="col-1"></div>
      </div>

      <div class="row">
        <div class="col-1"></div>
        <div class="col-5">
          <Card
                :title="t('title_invoices')"
                :description="t('description_invoices')"
                :icon="faReceipt"
                :actions="[{to : 'invoices', label : t('to_access') }]"
              >
            </Card>
        </div>
        <div class="col-5"></div>
        <div class="col-1"></div>
      </div>
    </div>
</template>

<style scoped>

</style>