// src/pages/PatientList.tsx
import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Tag, Spin, Typography } from 'antd';
import { EditOutlined, DeleteOutlined, PlusOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { getPatients, Patient } from '../api/patients';

const { Title } = Typography;

export default function PatientList() {
  const [data, setData]       = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const nav = useNavigate();

  useEffect(() => {
    getPatients()
      .then((res) => {
        // either an array, or { results: Patient[] }
        const arr: Patient[] = Array.isArray(res)
          ? res
          : (res as { results?: Patient[] }).results ?? [];
        setData(arr);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const columns = [
    {
      title: 'MRN',
      dataIndex: 'medical_record_number',
      key: 'medical_record_number',
      width: 150,
      fixed: 'left' as const,
    },
    {
      title: 'First Name',
      dataIndex: 'first_name',
      key: 'first_name',
      sorter: (a: Patient, b: Patient) =>
        (a.first_name ?? '').localeCompare(b.first_name ?? ''),
    },
    {
      title: 'Last Name',
      dataIndex: 'last_name',
      key: 'last_name',
      sorter: (a: Patient, b: Patient) =>
        (a.last_name ?? '').localeCompare(b.last_name ?? ''),
    },
    {
      title: 'DOB',
      dataIndex: 'date_of_birth',
      key: 'date_of_birth',
      sorter: (a: Patient, b: Patient) => {
        const aTime = a.date_of_birth
          ? new Date(a.date_of_birth).getTime()
          : 0;
        const bTime = b.date_of_birth
          ? new Date(b.date_of_birth).getTime()
          : 0;
        return aTime - bTime;
      },
      render: (d: string) => d || '—',
    },
    {
      title: 'Gender',
      dataIndex: 'gender',
      key: 'gender',
      filters: [
        { text: 'Male',   value: 'male' },
        { text: 'Female', value: 'female' },
      ],
      onFilter: (value: any, record: Patient) =>
        record.gender != null && record.gender === value,
      render: (g: string) =>
        g ? <Tag color={g === 'male' ? 'blue' : 'pink'}>{g}</Tag> : '—',
    },
    {
      title: 'Room',
      dataIndex: 'room_number',
      key: 'room_number',
      width: 100,
      render: (r: string | number | undefined) => r ?? '—',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      filters: [
        { text: 'Checked In', value: 'checked_in' },
        { text: 'Discharged', value: 'discharged' },
      ],
      onFilter: (value: any, record: Patient) =>
        record.status != null && record.status === value,
      render: (s: string) =>
        s ? (
          <Tag color={s === 'checked_in' ? 'green' : 'gray'}>
            {s.replace('_', ' ')}
          </Tag>
        ) : '—',
    },
    {
      title: 'Actions',
      key: 'actions',
      fixed: 'right' as const,
      width: 150,
      render: (_: any, record: Patient) => (
        <Space>
          <Button
            icon={<EditOutlined />}
            onClick={() => nav(`/patients/${record.id}/edit`)}
          />
          <Button
            icon={<DeleteOutlined />}
            danger
            onClick={() => {
              /* TODO: confirm + delete */
            }}
          />
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24, background: '#f5f7fa' }}>
      <Space style={{ marginBottom: 16 }}>
        <Title level={3}>Patient List</Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => nav('/patients/new')}
        >
          New Patient
        </Button>
      </Space>

      {loading ? (
        <Spin />
      ) : (
        <Table
          rowKey="id"
          columns={columns}
          dataSource={data}
          scroll={{ x: 1200 }}
          pagination={{ pageSize: 10 }}
        />
      )}
    </div>
  );
}
