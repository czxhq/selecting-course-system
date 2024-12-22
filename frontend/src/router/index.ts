import { useToken } from '@/store/token'
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/test',
      component: () => import('../views/test.vue')
    },
    {
      path: '/login',
      component: () => import('../views/login/my-login.vue')
    },
    {
      path: '/teacher-login',
      component: () => import('../views/login/teacher-login.vue')
    },
    {
      path: '/admin-login',
      component: () => import('../views/login/admin-login.vue')
    },
    {
      path: '/home',
      component: () => import('@/views/home/home.vue'),
      children: [
        {
          path: '/home/about',
          component: () => import('@/views/home/homeAbout.vue')
        },
        {
          path: '/home',
          component: () => import('@/views/home/homePage.vue')
        },
        {
          path: '/home/help',
          component: () => import('@/views/home/homeHelp.vue')
        }
      ]
    },
    {
      path: '/main',
      component: () => import('../views/main/my-main.vue'),
      children: [
        {
          path: '/main/courses',
          component: () => import('@/views/main/mainCourses.vue')
        },
        {
          path: '/main/courses/:courseId',
          name: 'course-detail',
          component: () => import('@/views/main/CourseDetails.vue')
        },
        {
          path: '/main',
          component: () => import('@/views/main/mainPage.vue')
        },
        {
          path: '/main/help',
          component: () => import('@/views/main/mainHelp.vue')
        }
      ],
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/admin',
      component: () => import('../views/admin/admin.vue'),
      meta: {
        requiresAdminAuth: true
      }
    },
    {
      path: '/teacher-page',
      component: () => import('../views/teacher/teacherPage.vue'),
      meta: {
        requiresTeacherAuth: true
      }
    },
    {
      path: '/teacher-page/:courseId',
      name: 'CourseDetail',
      component: () => import('@/views/teacher/CouseDetails.vue'),
      meta: {
        requiresTeacherAuth: true
      }
    },
    {
      path: '/:pathMatch(.*)',
      component: () => import('../views/404/NotFound.vue'),
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (
    to.meta.requiresAuth &&
    (!localStorage.getItem('token') ||
      localStorage.getItem('token') === 'undefined' ||
      localStorage.getItem('token') !== 'stu')
  ) {
    next({ path: '/login' })
  } else if (
    to.meta.requiresTeacherAuth &&
    (!localStorage.getItem('token') ||
      localStorage.getItem('token') === 'undefined' ||
      localStorage.getItem('token') !== 'tea')
  ) {
    next({ path: '/teacher-login' })
  } else if (
    to.meta.requiresAdminAuth &&
    (!localStorage.getItem('token') ||
      localStorage.getItem('token') === 'undefined' ||
      localStorage.getItem('token') !== 'adm')
  ) {
    next({ path: '/admin-login' })
  } else {
    next()
  }
})

export default router
