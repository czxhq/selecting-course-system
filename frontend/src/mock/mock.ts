import Mock from 'mockjs'

// 定义 mock 数据
const Random = Mock.Random
const BASE_URL = 'http://localhost:5173'

Mock.setup({
  timeout: '200-600' // 设置模拟接口响应时间
})

// 模拟 GET 请求 /api/user
Mock.mock('/api/login/', 'post', {
  code: 200,
  message: 'success',
  result: 'success'
})

// 6.3 获取教师课表
Mock.mock('/api/home/teacherCourses/', 'post', (req) => {
  const { TeacherId } = JSON.parse(req.body)

  // 模拟返回一个教师的课程表
  return {
    data: {
      courses: [
        {
          courseId: 'C1001',
          courseName: '高等数学',
          location: '教室A101',
          time: ['1 1-2 1-3']
        },
        {
          courseId: 'C1002',
          courseName: '英语',
          location: '教室B102',
          time: ['7 2-4 1-16']
        }
      ]
    }
  }
})

Mock.mock('/api/home/courses/', 'post', {
  code: 200,
  message: 'success',
  data: {
    courses: [
      {
        courseId: '1',
        courseName: '高等数学',
        teacher: '张老师',
        location: '教室A101',
        time: ['1 1-2 1-3'] //周几 第几节到第几节，第几周到第几周 用-连接
      },
      {
        courseId: '2',
        courseName: '英语',
        teacher: '李老师',
        location: '教室B102',
        time: ['7 2-4 1-16']
      },
      {
        courseId: '3',
        courseName: '博雅',
        teacher: '李老师',
        location: '教室B104',
        time: ['7 5-7 1-16']
      }
    ]
  }
})

Mock.mock('/api/home/messages/', 'post', {
  code: 200,
  message: 'success',
  data: {
    messages: [
      {
        title: '课程调整通知',
        date: '2024-11-15',
        content: '由于特殊原因，周四的数学课将调整为周五。',
        from: '课程名称'
      },
      {
        title: '课程调整通知',
        date: '2024-11-17',
        content: '由于特殊原因，周四的数学课将调整为周五。',
        from: '课程名称'
      }
    ]
  }
})

Mock.mock('/api/home/courseSelect/', 'post', {
  code: 200,
  message: 'success',
  courses: [
    {
      courseId: 'C1001',
      courseName: '高等数学',
      teacher: '张老师',
      location: '教室A101',
      time: ['1 1-2 1-3', '3 4-5 4-13'], //周几 第几节到第几节，第几周到第几周 用-连接
      type: '必修',
      category: 'GM', //代码参考文档
      capacity: '50/40' //容量/已选
    },
    {
      courseId: 'C1002',
      courseName: '英语',
      teacher: '李老师',
      location: '教室B102',
      time: ['1 1-2 1-3'], //周几 第几节到第几节，第几周到第几周 用-连接
      type: '选修',
      category: 'GM',
      capacity: '30/25'
    }
  ]
})

Mock.mock('/api/courses/cancelCourse/', 'post', {
  code: 200,
  message: 'success',
  result: 'success'
})

// 1.0 获取所有课程
Mock.mock('/api/courses/allCourse/', 'post', () => {
  return {
    courses: [
      {
        courseId: 'C1001',
        courseName: '高等数学',
        teacher: '张老师',
        location: '教室A101',
        time: ['1 1-2 1-3', '2 3-4 2-4'],
        type: '必修',
        category: 'GM',
        capacity: '50/40'
      },
      {
        courseId: 'C1002',
        courseName: '英语',
        teacher: '李老师',
        location: '教室B102',
        time: ['1 1-2 1-3'],
        type: '选修',
        category: 'GM',
        capacity: '30/25'
      },
      {
        courseId: 'C1003',
        courseName: '计算机科学导论',
        teacher: '王老师',
        location: '教室C201',
        time: ['3 1-2 3-4'],
        type: '必修',
        category: 'CS',
        capacity: '40/35'
      },
      {
        courseId: 'C1004',
        courseName: '数据结构与算法',
        teacher: '赵老师',
        location: '教室D102',
        time: ['4 2-3 1-2', '5 3-4 1-3'],
        type: '必修',
        category: 'CS',
        capacity: '50/48'
      },
      {
        courseId: 'C1005',
        courseName: '微积分',
        teacher: '钱老师',
        location: '教室A103',
        time: ['2 2-3 2-3'],
        type: '必修',
        category: 'GM',
        capacity: '60/55'
      },
      {
        courseId: 'C1006',
        courseName: '物理',
        teacher: '孙老师',
        location: '教室B104',
        time: ['3 1-2 1-3'],
        type: '选修',
        category: 'GM',
        capacity: '45/42'
      },
      {
        courseId: 'C1007',
        courseName: '高等代数',
        teacher: '李老师',
        location: '教室A202',
        time: ['1 3-4 1-2', '2 1-2 3-4'],
        type: '必修',
        category: 'GM',
        capacity: '50/45'
      },
      {
        courseId: 'C1008',
        courseName: '线性代数',
        teacher: '刘老师',
        location: '教室B103',
        time: ['4 2-3 2-4'],
        type: '必修',
        category: 'GM',
        capacity: '60/50'
      },
      {
        courseId: 'C1009',
        courseName: '英语口语',
        teacher: '陈老师',
        location: '教室C104',
        time: ['2 1-2 3-4'],
        type: '选修',
        category: 'GM',
        capacity: '30/20'
      },
      {
        courseId: 'C1010',
        courseName: '数据库原理',
        teacher: '冯老师',
        location: '教室D201',
        time: ['5 1-2 3-4'],
        type: '必修',
        category: 'CS',
        capacity: '40/38'
      },
      {
        courseId: 'C1011',
        courseName: '概率论',
        teacher: '钱老师',
        location: '教室B105',
        time: ['3 3-4 1-2'],
        type: '必修',
        category: 'GM',
        capacity: '55/50'
      },
      {
        courseId: 'C1012',
        courseName: '人工智能',
        teacher: '李老师',
        location: '教室C203',
        time: ['1 2-3 2-4'],
        type: '选修',
        category: 'CS',
        capacity: '30/25'
      },
      {
        courseId: 'C1013',
        courseName: '数据科学与机器学习',
        teacher: '赵老师',
        location: '教室D301',
        time: ['4 3-4 1-2', '5 1-2 2-3'],
        type: '选修',
        category: 'CS',
        capacity: '40/35'
      },
      {
        courseId: 'C1014',
        courseName: '操作系统',
        teacher: '张老师',
        location: '教室A301',
        time: ['2 2-3 3-4'],
        type: '必修',
        category: 'CS',
        capacity: '50/45'
      },
      {
        courseId: 'C1015',
        courseName: '计算机网络',
        teacher: '王老师',
        location: '教室B201',
        time: ['3 1-2 1-3'],
        type: '选修',
        category: 'CS',
        capacity: '45/40'
      },
      {
        courseId: 'C1016',
        courseName: '现代通信原理',
        teacher: '孙老师',
        location: '教室C301',
        time: ['4 3-4 2-3'],
        type: '选修',
        category: 'EE',
        capacity: '35/30'
      },
      {
        courseId: 'C1017',
        courseName: '数字电路',
        teacher: '李老师',
        location: '教室D302',
        time: ['2 3-4 1-2', '3 1-2 4-5'],
        type: '选修',
        category: 'EE',
        capacity: '40/35'
      },
      {
        courseId: 'C1018',
        courseName: '信号与系统',
        teacher: '赵老师',
        location: '教室A402',
        time: ['1 1-2 2-3'],
        type: '必修',
        category: 'EE',
        capacity: '50/45'
      },
      {
        courseId: 'C1019',
        courseName: '电路原理',
        teacher: '钱老师',
        location: '教室B403',
        time: ['2 1-2 3-4'],
        type: '选修',
        category: 'EE',
        capacity: '30/28'
      },
      {
        courseId: 'C1020',
        courseName: '微观经济学',
        teacher: '陈老师',
        location: '教室C404',
        time: ['5 2-3 1-2'],
        type: '选修',
        category: 'ECO',
        capacity: '40/36'
      }
    ]
  }
})

// 2.0 搜索课程
Mock.mock('/api/courses/search/', 'post', (options) => {
  const { query, type } = JSON.parse(options.body)
  console.log(query, type)
  // 模拟搜索课程，根据 `query` 和 `type` 参数
  const courses = [
    {
      courseId: 'C1001',
      courseName: '高等数学',
      teacher: '张老师',
      location: '教室A101',
      time: ['1 1-2 1-3'],
      type: '必修',
      category: 'GM',
      capacity: '50/40'
    },
    {
      courseId: 'C1002',
      courseName: '英语',
      teacher: '李老师',
      location: '教室B102',
      time: ['1 1-2 1-3'],
      type: '选修',
      category: 'GM',
      capacity: '30/25'
    }
  ]

  if (type === 0) {
    // 按课程名查询
    return {
      courses: courses.filter((course) => course.courseName.includes(query))
    }
  } else if (type === 1) {
    // 按教师名查询
    return {
      courses: courses.filter((course) => course.teacher.includes(query))
    }
  }

  return { courses }
})

// 3.0 查看课程详情
Mock.mock('/api/courses/get/', 'post', (options) => {
  const { courseId } = JSON.parse(options.body)

  const courseDetails = {
    C1001: {
      courseName: '高等数学',
      teacher: '张老师',
      location: '教室A101',
      time: ['1 1-2 1-3'],
      type: '必修',
      category: 'GM',
      capacity: '50/40',
      courseDetails: '这是高等数学课程的详细描述。',
      teacherInfo: '张老师，教授，拥有10年教学经验。',
      courseReview: [
        {
          student: '王学生',
          rating: 4,
          comment: '课程内容丰富，但节奏较快。'
        },
        {
          student: '陈学生',
          rating: 3,
          comment: '给分一般'
        },
        {
          student: '陈学生',
          rating: 3,
          comment: '作业太多'
        },
        {
          student: '张学生',
          rating: 4,
          comment: '还行'
        }
      ],
      courseQnA: [
        {
          id: '222',
          question: '这门课程需要什么先修知识？',
          answer: '需要有一定的数学基础。'
        },
        {
          id: '224',
          question: '这门课给分高吗？',
          answer: '看老师心情'
        }
      ]
    },
    C1002: {
      courseName: '英语',
      teacher: '李老师',
      location: '教室B102',
      time: ['1 1-2 1-3'],
      type: '选修',
      category: 'GM',
      capacity: '30/25',
      courseDetails: '这是英语课程的详细描述。',
      teacherInfo: '李老师，讲授英语课程已有15年。',
      courseReview: [
        {
          student: '张学生',
          rating: 5,
          comment: '非常喜欢这门课，英语进步了很多。'
        }
      ],
      courseQnA: [
        {
          id: '223',
          question: '这门课程有语法相关内容吗？',
          answer: '有，主要讲解基础语法知识。'
        }
      ]
    }
  }

  return { data: {} }
})

// 4.0 发布问题
Mock.mock('/api/courses/question/', 'post', (options) => {
  const { courseId } = JSON.parse(options.body)

  // 模拟问题发布成功
  return {
    result: 'success'
  }
})

// 5.0 选择课程
Mock.mock('/api/courses/selectCourse/', 'post', (options) => {
  const { courseId, studentId } = JSON.parse(options.body)

  // 模拟课程选择成功
  return {
    result: 'success'
  }
})
// 4.1 搜索功能
Mock.mock('/api/admin/search/', 'post', (req) => {
  const { query, type, by } = JSON.parse(req.body)
  const students = [
    { Id: '20230001', name: '张三' },
    { Id: '20202123', name: '李老' }
  ]
  const teachers = [
    { Id: 'T1001', name: '王老师' },
    { Id: 'T1002', name: '赵老师' }
  ]

  // 根据搜索条件过滤数据
  let result = []
  if (type === 0) {
    // 查学生
    result = students.filter(
      (item) => item.name.includes(query) || item.Id.includes(query)
    )
  } else {
    // 查教师
    result = teachers.filter(
      (item) => item.name.includes(query) || item.Id.includes(query)
    )
  }

  return {
    data: result
  }
})

// 4.2 发布通知
Mock.mock('/api/admin/notifications/', 'post', (req) => {
  const { title, content } = JSON.parse(req.body)

  // 模拟发布成功/失败
  if (title && content) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 4.3 获取历史通知
Mock.mock('/api/admin/getNotifications/', 'post', () => {
  const messages = [
    {
      title: '课程调整通知',
      date: '2024-11-15',
      content: '由于特殊原因，周四的数学课将调整为周五。'
    },
    {
      title: '寒假放假通知',
      date: '2024-12-01',
      content: '学校安排寒假放假，具体时间请关注通知。'
    }
  ]

  return {
    data: {
      messages
    }
  }
})

// 4.4 导入学生
Mock.mock('/api/admin/importStudent/', 'post', (req) => {
  const { id, name } = JSON.parse(req.body)

  // 模拟导入成功/失败
  if (id && name) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 4.5 导入教师
Mock.mock('/api/admin/importTeacher/', 'post', (req) => {
  const { id, name } = JSON.parse(req.body)

  // 模拟导入成功/失败
  if (id && name) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 4.6 重置密码
Mock.mock('/api/admin/reset/', 'post', (req) => {
  const { type, id } = JSON.parse(req.body)

  // 模拟重置密码成功/失败
  if (type === 0 || type === 1) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 4.7 删除教师
Mock.mock('/api/admin/deleteTeacher/', 'post', (req) => {
  const { id } = JSON.parse(req.body)

  // 模拟删除成功/失败
  if (id) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 4.8 删除学生
Mock.mock('/api/admin/deleteStudent/', 'post', (req) => {
  const { id } = JSON.parse(req.body)

  // 模拟删除成功/失败
  if (id) {
    return {
      result: 'success'
    }
  } else {
    return {
      result: 'failed'
    }
  }
})

// 获取所有学生
Mock.mock('/api/admin/getAllStudent/', 'post', {
  data: [
    {
      Id: '20230001',
      name: '张三'
    },
    {
      Id: '20202123',
      name: '李老'
    }
  ]
})

// 获取所有教师
Mock.mock('/api/admin/getAllTeacher/', 'post', {
  data: [
    {
      Id: '20230001',
      name: '张三'
    },
    {
      Id: '20202123',
      name: '李老'
    }
  ]
})

// 6.1 发布课程
Mock.mock('/api/teacher/publishCourse/', 'post', (req) => {
  const {
    teahcerId,
    courseId,
    courseName,
    time,
    location,
    capacity,
    type,
    category,
    courseDetails
  } = JSON.parse(req.body)

  // 这里模拟一个课程发布成功或失败的结果
  const result = Math.random() > 0.5 ? 'success' : 'failed'

  return {
    result
  }
})

// 6.2 发布通知
Mock.mock('/api/teacher/notifications/', 'post', (req) => {
  const { courseId, title, content } = JSON.parse(req.body)

  // 模拟通知发布成功或失败
  const result = Math.random() > 0.5 ? 'success' : 'failed'

  return {
    result
  }
})

// 6.4 修改课程
Mock.mock('/api/teacher/alterCourse/', 'post', (req) => {
  const {
    courseId,
    courseName,
    time,
    location,
    capacity,
    type,
    category,
    courseDetails
  } = JSON.parse(req.body)

  // 模拟课程修改成功或失败
  const result = Math.random() > 0.5 ? 'success' : 'failed'

  return {
    result
  }
})

// 6.5 删除课程
Mock.mock('/api/teacher/deleteCourse/', 'post', (req) => {
  const { courseId } = JSON.parse(req.body)

  // 模拟删除课程成功或失败
  const result = Math.random() > 0.5 ? 'success' : 'failed'

  return {
    result
  }
})

// 6.6 回答问题
Mock.mock('/api/teacher/answer/', 'post', (req) => {
  const { id, answer } = JSON.parse(req.body)

  // 模拟问题回答成功或失败
  const result = Math.random() > 0.5 ? 'success' : 'failed'

  return {
    result
  }
})

Mock.mock('/api/teacher/question/', 'post', (options) => {
  const { courseId } = JSON.parse(options.body)

  // 模拟问题列表
  const mockData = {
    result: [
      {
        id: '1',
        question: '这门课程需要什么先修知识？'
      },
      {
        id: '2',
        question: '课程的作业量如何？'
      },
      {
        id: '3',
        question: '是否有线上学习平台？'
      },
      {
        id: '4',
        question: '这门课程的考试形式是什么？'
      }
    ]
  }

  // 根据不同的课程 ID 返回不同的问题列表
  if (courseId === 'math101') {
    mockData.result = [
      {
        id: '1',
        question: '这门课程需要什么数学基础？'
      },
      {
        id: '2',
        question: '课程中有无编程相关内容？'
      }
    ]
  } else if (courseId === 'cs101') {
    mockData.result = [
      {
        id: '1',
        question: '这门课程是否需要自学一些编程语言？'
      },
      {
        id: '2',
        question: '课程内容包括算法吗？'
      }
    ]
  }

  // 返回模拟数据
  return mockData
})

Mock.mock('/api/teacher-login/', 'post', {
  code: 200,
  message: 'success',
  result: 'success'
})

Mock.mock('/api/admin-login/', 'post', {
  code: 200,
  message: 'success',
  result: 'success'
})
console.log('Mock server is running...')
export default {}
