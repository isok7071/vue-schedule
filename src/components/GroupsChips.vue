        
<template>
    <v-chip-group
        selected-class="text-primary"
        column
    >
        <template
            v-for="id, group in groups"
            :key="id"
        >

            <v-chip
                filter
                @click="store.toggleSelected(group)"
            >
                {{ group }}
            </v-chip>
        </template>



        <v-progress-linear
            indeterminate
            color="primary"
            :height="10"
            v-if="isLoading"
        ></v-progress-linear>
    </v-chip-group>
</template>

<script lang="ts" setup>
import { useAppStore } from '@/store/app';
import { storeToRefs } from 'pinia';

const store = useAppStore()
const { isLoading, groups } = storeToRefs(store)

store.getGroups()

</script>