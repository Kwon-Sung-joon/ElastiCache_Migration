# ElastiCache_Migration

- idc redis 서버의 데이터를 AWS ElastiCache로 데이터 이관


## 사전 조건
- VPN 또는 DX를 통한 AWS VPC와 IDC 간 연결 필요
- 해당 코드는 Lambda 기반으로 Lambda를 VPC 내부에 생성 필요
- redis 사용에 필요한 라이브러리 구성 필요
